from crewai import Crew
from agents.planner import planner, make_task
from agents.reviewer import reviewer
from agents.test_writer import test_writer
from agents.devops import devops

# tente carregar o Explorer
try:
    from agents.explorer import explorer
    AGENTS = [planner, reviewer, test_writer, devops, explorer]
except SystemExit:
    AGENTS = [planner, reviewer, test_writer, devops]

crew = Crew(agents=AGENTS)

def handle_pr(pr_url: str):
    crew.run(make_task(pr_url))