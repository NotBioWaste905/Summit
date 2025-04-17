from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from colorama import Fore
from pathlib import Path

from prompts import discussion_start, discussion_finish
from itertools import cycle


class Discussion:
    """A class to facilitate and manage a structured multi-turn discussion among participants.

    Attributes:
        participants (dict[str, dict]): A dictionary where keys are participant names and values are dictionaries
            containing participant-specific data, such as their model and status.
        topic (str): The topic of the discussion.
        global_context (list): A list to store global context information for the discussion.
        max_turns (int): The maximum number of turns allowed in the discussion.
        messages (list): A list of messages exchanged during the discussion, starting with a system prompt.

    Methods:
        __init__(participants: dict[str, dict], topic: str):
            Initializes the Discussion instance with participants, topic, and default settings.

        run():
            Orchestrates the discussion among participants, handling message exchanges, participant responses,
            and generating a summary if applicable. Saves the discussion to a markdown file upon completion.
    """

    def __init__(self, participants: dict[str, dict], topic: str):
        # Initialize participants and topic
        self.participants = participants
        self.topic = topic

        # Initialize discussion settings
        self.global_context = []
        self.max_turns = 10

        # Initialize message history with the starting prompt
        self.messages = [
            SystemMessage(content=discussion_start.format(topic=self.topic)),
        ]

        print(f"Discussion initialized with topic: {self.topic}")

    def run(self):
        """
        Run the discussion.

        This method orchestrates a multi-turn discussion among participants. Each participant
        takes turns responding to the discussion context until the maximum number of turns is
        reached or all participants indicate they have nothing more to add.

        Parameters:
        None

        Expected Behavior:
        - Iterates through the participants for a maximum of `max_turns`.
        - Each participant's response is appended to the discussion messages.
        - Responses are printed in different colors for specific participants.
        - If a participant's response contains "I have nothing to add to the discussion.",
          they are marked as finished and will not contribute further.
        - At the end of the discussion, a summary is generated if "Alice" is a participant.
        """
        # Define a cycle of colors for participants
        color_palette = cycle(
            [Fore.RED, Fore.GREEN, Fore.BLUE, Fore.CYAN, Fore.MAGENTA, Fore.WHITE]
        )
        colors = {name: next(color_palette) for name in self.participants.keys()}
        colors["Summary"] = Fore.YELLOW  # Ensure the summary color remains yellow

        for i in range(self.max_turns):
            for name, participant in self.participants.items():
                # Get the participant's response
                if participant["finished"]:
                    continue
                response = participant["model"].invoke(self.messages)

                # Add the response to the messages
                self.messages.append(
                    HumanMessage(content=f"{name}: {response.content}")
                )
                # Print the response with the corresponding color
                color = colors.get(name, Fore.RESET)
                print(color + f"{name}: {response.content}" + Fore.RESET)
                if "I have nothing to add to the discussion." in str(response.content):
                    participant["finished"] = True
                    print(f"{name} has finished the discussion.")
                print("\n")

        # Summarize the discussion
        if "Alice" in self.participants:
            summary = self.participants["Alice"]["model"].invoke(
                self.messages + [SystemMessage(discussion_finish.format())]
            )
            print(Fore.YELLOW + f"Summary: {summary.content}" + Fore.RESET)
        else:
            print(
                Fore.YELLOW
                + "Summary: Unable to summarize as 'Alice' is not a participant."
                + Fore.RESET
            )
        print("Discussion finished.")

        # Create discussions directory if it doesn't exist
        discussions_dir = Path("discussions")
        discussions_dir.mkdir(exist_ok=True)

        # Save to markdown file with good formatting
        filename = f"{self.topic.replace(' ', '_').lower()}.md"
        filepath = discussions_dir / filename
        with open(filepath, "w") as f:
            f.write(f"# Discussion on: {self.topic}\n\n")
            f.write("## Participants:\n")
            for name in self.participants.keys():
                f.write(f"- {name}\n")
            f.write("\n## Discussion:\n")
            for message in self.messages:
                if isinstance(message, HumanMessage):
                    f.write(f"- **{message.content}**\n")
                elif isinstance(message, SystemMessage):
                    f.write(f"- *{message.content}*\n")
                elif isinstance(message, AIMessage):
                    f.write(f"- {message.content}\n")
            f.write("\n## Summary:\n")
            f.write(f"- {summary.content}\n")

        print(f"Discussion saved to {filepath}")
