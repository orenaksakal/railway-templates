"""Private, single-process AgentScope service; upstream API, no demo credentials."""
import os
from agentscope.app import create_app
from agentscope.app.storage import RedisStorage
from agentscope.app.workspace_manager import LocalWorkspaceManager
from agentscope.app.message_bus import InMemoryMessageBus
app = create_app(
    storage=RedisStorage(host=os.environ["REDIS_HOST"], port=6379,
                         password=os.environ["REDIS_PASSWORD"]),
    message_bus=InMemoryMessageBus(),
    workspace_manager=LocalWorkspaceManager(basedir="/data/workspaces", default_mcps=[]),
)
