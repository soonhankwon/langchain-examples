import asyncio
import json
import os
from typing import Any, Dict
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.server.lowlevel.server import NotificationOptions
from mcp.types import (
    CallToolResult,
    ListToolsResult,
    Tool,
    TextContent,
)
from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate

# 환경 변수 로드
load_dotenv()

app = FastAPI(title="Supabase User MCP Server", version="1.0.0")

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_ANON_KEY")

if not supabase_url or not supabase_key:
    raise ValueError("SUPABASE_URL과 SUPABASE_ANON_KEY 환경 변수가 필요합니다.")

supabase: Client = create_client(supabase_url, supabase_key)

# Pydantic 모델들
class User(BaseModel):
    id: int
    nickname: str
    email: str

# FastAPI 엔드포인트
@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    """특정 유저 정보를 가져옵니다."""
    try:
        response = supabase.table("user").select("*").eq("id", user_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"유저 정보 조회 실패: {str(e)}")

# MCP 서버 설정
server = Server("supabase-user-mcp")

@server.list_tools()
async def handle_list_tools() -> ListToolsResult:
    """사용 가능한 도구들을 나열합니다."""
    return ListToolsResult(
        tools=[
            Tool(
                name="get_user_by_id",
                description="특정 ID의 유저 정보를 가져옵니다.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "integer",
                            "description": "조회할 유저의 ID"
                        }
                    },
                    "required": ["user_id"]
                }
            )
        ]
    )

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """도구를 호출합니다."""
    try:
        if name == "get_user_by_id":
            user_id = arguments["user_id"]
            response = supabase.table("user").select("*").eq("id", user_id).execute()
            if not response.data:
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text=f"ID {user_id}의 유저를 찾을 수 없습니다."
                        )
                    ]
                )
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"유저 정보:\n{json.dumps(response.data[0], indent=2, ensure_ascii=False)}"
                    )
                ]
            )
        
        else:
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"알 수 없는 도구: {name}"
                    )
                ]
            )
    
    except Exception as e:
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"오류 발생: {str(e)}"
                )
            ]
        )

async def main():
    """메인 함수"""
    print("Supabase User MCP 서버를 시작합니다...")
    
    # MCP 서버 시작
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="supabase-user-mcp",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(tools_changed=False),
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
