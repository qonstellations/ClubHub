from app.tui import text
from app.core.user import User, create_user, authenticate_user, get_user_clubs, get_user_role
from app.core.club import Club, create_club, club_member_count, get_club_channels
from app.core.channel import Channel, create_channel

# separate app imports from third party imports
from rich.console import Console, Group
from rich.table import Table
from rich.layout import Layout
from rich.prompt import Prompt
from rich.text import Text
from rich.columns import Columns
from app.tui.text import Panel

import os
import time

console = Console()

def clear_terminal():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def pause():
    time.sleep(2.5)

def welcome():
    clear_terminal()
    console.print(text.welcome)
    input("\nPress any key to continue to login page")
    login()

def login():
    clear_terminal()
    console.print(text.login)
    inp = int(input("Enter the option number: "))
    clear_terminal()

    match inp:
        case 1:
            email = str(input("Enter your E-mail: "))
            password1 = Prompt.ask("Enter a password: ", password=True, console=console)
            password2 = str(input("Confirm password: "))
            first_name = str(input("Enter your first name: "))
            last_name = str(input("Enter your last name: "))
            
            user = create_user(
                email=email, 
                password1=password1,
                password2=password2,
                first_name=first_name,
                last_name=last_name
            )

            if user is not None:
                console.print("\n[bold green]Account Successfully Created[/bold green]")
                console.print("[green]Redirecting to homepage...[/green]")
                pause()
                homepage(user)
            else:
                console.print("\n[bold red]Something went wrong, please try again![/bold red]")
                console.print("[yellow]Redirecting back to login...[/yellow]")
                pause()
                login()

        case 2: 
            email = str(input("Enter your E-mail: "))
            password = Prompt.ask("Enter a password: ", password=True, console=console)
            user = authenticate_user(email=email, password=password)

            if user is not None:
                console.print("\n[bold green]Logged in Successfully[/bold green]")
                console.print("[green]Redirecting to homepage...[/green]")
                pause()
                homepage(user)
            else:
                console.print("\n[bold red]Something went wrong, please try again![/bold red]")
                console.print("[yellow]Redirecting back to login...[/yellow]")
                pause()
                login()
            
        case 3:
            welcome()

        case _:
            console.print("\n[bold red]Please enter a valid input[/bold red]")
            console.print("[yellow]Redirecting back to login...[/yellow]")
            pause()
            login()

def homepage(user : User):
    clear_terminal()
    console.print(text.homepage)
    inp = int(input("Enter the option number: "))
    clear_terminal()

    match inp:
        case 1:
            name = str(input("Enter the name of the club: "))
            description = str(input("Enter the description for the club: "))
            club_code = str(input("Enter the club code: "))
            secret_key = str(input("Enter the secret key: "))

            club = create_club(
                name=name,
                description=description,
                club_code=club_code,
                secret_key=secret_key,
                creator_user_id=user._id
            )

            if club is not None:
                console.print("\n[bold green]Club Created Successfully!![/bold green]")
                console.print("[green]Redirecting to Clubpage...[/green]")
                pause()
                clubpage()
            else:
                console.print("\n[bold red]Something went wrong, please try again![/bold red]")
                console.print("[yellow]Redirecting back to Homepage...[/yellow]")
                pause()
                homepage(user)

        case 2:
            user_clubs = get_user_clubs(user=user)

            if user_clubs is None:
                console.print("\n[bold red]You are not part of any club. Please ask a club admin to add you![/bold red]")
                console.print("[yellow]Redirecting back to Homepage...[/yellow]")
                pause()
                homepage(user)
            else:
                club_cards = list()
                for index, club in enumerate(user_clubs, start=1):
                    content = Group(
                        Text(f"Role : {get_user_role(user, club).name}", style="bold", justify="center"),
                        Text(f"Description : {club.description}"),
                        Text(f"Total Members : {club_member_count(club)}"),
                    )

                    card = Panel(
                        content,
                        title=f"{club.name}",
                        border_style="blue",
                        subtitle=Text(f"Option {index}"),
                        subtitle_align="center",
                        width=30,
                        height=15
                    )
                    club_cards.append(card)

                console.print(
                    Panel(
                        Text("Your Clubs", justify="center", style="bold"),
                        border_style="green",
                        padding=(0, 1)
                    )
                )
                console.print(Columns(club_cards, align="center", expand=False))

            club_index = int(input("\nEnter Option Number : "))
            if club_index < 1 or club_index > len(club_cards):
                console.print("\n[bold red]Please fill a valid input[/bold red]")
                console.print("[yellow]Redirecting back to homepage...[/yellow]")
                pause()
                homepage(user)
            else:
                clubpage(user=user, club=user_clubs[club_index-1])

        case 3:
            console.print("\n[yellow]Feature will be added later[/yellow]")
            console.print("[yellow]Redirecting back to homepage...[/yellow]")
            pause()
            homepage(user)

        case _:
            console.print("\n[bold red]Please fill a valid input[/bold red]")
            console.print("[yellow]Redirecting back to homepage...[/yellow]")
            pause()
            homepage(user)

def clubpage(user : User, club : Club):
    clear_terminal()
    console.print(Panel(Text(club.name, justify="center")))
    console.print(text.clubpage)
    inp = int(input("Enter the option number: "))
    clear_terminal()

    match inp:
        case 1:
            channels = get_club_channels(club=club)
            console.print(
                    Panel(
                        Text("All Channels", justify="center", style="bold"),
                        border_style="green",
                        padding=(0, 1)
                    )
                )

            if channels is None:
                console.print(
                    Panel(
                        Text("You don't have any channels to view!\nReturning to clubpage...", 
                            justify="center", style="bold"),
                        border_style="red",
                        padding=(0, 1)
                    )
                )
                pause()
                clubpage(user=user, club=club)
            else:
                for index, channel in enumerate(channels, start=1):
                    console.print(Text(f"[{index}] {channel.name}", style="bold"))

                channel_index = int(input("\nEnter Option Number : "))
                if channel_index < 1 or channel_index > len(channels):
                    console.print("\n[bold red]Please fill a valid input[/bold red]")
                    console.print("[yellow]Redirecting back to homepage...[/yellow]")
                    pause()
                    clubpage(user=user, club=club)
                else:
                    # redirect to channels
                    console.print("\n[yellow]Feature will be added later[/yellow]")
                    console.print("[yellow]Redirecting back to clubpage...[/yellow]")
                    pause()
                    clubpage(user=user, club=club)
                    

        case 2:
            console.print("\n[yellow]Feature will be added later[/yellow]")
            console.print("[yellow]Redirecting back to clubpage...[/yellow]")
            pause()
            clubpage(user=user, club=club)
        
        case 3:
            console.print("\n[yellow]Feature will be added later[/yellow]")
            console.print("[yellow]Redirecting back to clubpage...[/yellow]")
            pause()
            clubpage(user=user, club=club)

        case 4:
            name = str(input("Enter channel name : "))
            channel = create_channel(club=club, name=name, user=user)

        case 5:
            homepage(user=user)

        case _:
            console.print("\n[bold red]Please fill a valid input[/bold red]")
            console.print("[yellow]Redirecting back to clubpage...[/yellow]")
            pause()
            clubpage(user=user, club=club)

def view_channel(channel : Channel):
    return
