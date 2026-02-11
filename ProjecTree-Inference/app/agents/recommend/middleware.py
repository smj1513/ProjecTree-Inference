from langchain.agents.middleware import AgentMiddleware
from langchain.tools.tool_node import ToolCallRequest
from langchain.messages import ToolMessage
from langgraph.types import Command
from typing import Callable

class SearchDomainMiddleware(AgentMiddleware):
    def __init__(self, allowed_domains: list[str]):
        """
        검색 도구의 도메인을 제한하는 미들웨어
        Args:
            allowed_domains: 허용할 도메인 리스트
        """
        super().__init__()
        self.allowed_domains = allowed_domains

    def wrap_tool_call(
        self,
        request: ToolCallRequest,
        handler: Callable[[ToolCallRequest], ToolMessage | Command],
    ) -> ToolMessage | Command:
        # 호출된 도구가 'restricted_search' 인지 확인
        if request.tool_call['name'] == 'restricted_search':
            # args에 include_domains 주입 (기존 args는 유지)
            new_args = request.tool_call['args'].copy()
            new_args['include_domains'] = self.allowed_domains
            
            # request의 tool_call args 업데이트
            request.tool_call['args'] = new_args
            
        return handler(request)
