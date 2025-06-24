

from rich.live import Live
from rich.text import Text
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.layout import Layout
from typing_master.words import beginner_words, intermediate_words, advanced_words
import keyboard
import time
import random
import threading
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any

console = Console()

# File to store scoreboard data
SCOREBOARD_FILE = "typing_scores.json"

def load_scoreboard() -> List[Dict[str, Any]]:
    """Load existing scoreboard data"""
    if os.path.exists(SCOREBOARD_FILE):
        try:
            with open(SCOREBOARD_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def save_score(player_name: str, wpm: float, accuracy: float, difficulty: int, time_limit: int) -> None:
    """Save score to scoreboard"""
    scores = load_scoreboard()
    new_score = {
        "name": player_name,
        "wpm": round(wpm, 1),
        "accuracy": round(accuracy, 1),
        "difficulty": ["Beginner", "Intermediate", "Advanced"][difficulty-1],
        "time_limit": time_limit,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    scores.append(new_score)
    
    # Keep only top 20 scores
    scores = sorted(scores, key=lambda x: x['wpm'], reverse=True)[:20]
    
    with open(SCOREBOARD_FILE, 'w') as f:
        json.dump(scores, f, indent=2)

def animated_text_display(text: str, style: str = "bold bright_cyan", delay: float = 0.03) -> Text:
    """Display text with typing animation"""
    animated_text = Text()
    with Live(animated_text, refresh_per_second=30, console=console) as live:
        for char in text:
            animated_text.append(char, style=style)
            live.update(animated_text)
            time.sleep(delay)
    return animated_text

def show_animated_welcome() -> None:
    """Display animated welcome message"""
    console.clear()
    
    # Animated title
    title_lines = [
        "╔═══════════════════════════════════════╗",
        "║          🚀 TYPING MASTER ⚡          ║",
        "║     Terminal Edition with Style       ║",
        "╚═══════════════════════════════════════╝"
    ]
    
    for line in title_lines:
        animated_text_display(line + "\n", style="bold bright_cyan", delay=0.01)
    
    # Animated subtitle
    time.sleep(0.5)
    animated_text_display("\n✨ Test your typing speed and accuracy! ✨\n", 
                         style="italic bright_yellow", delay=0.02)
    
    # Loading animation
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]Loading awesome features..."),
        console=console,
    ) as progress:
        task = progress.add_task("", total=100)
        for i in range(100):
            progress.update(task, advance=1)
            time.sleep(0.01)
    
    time.sleep(0.5)

def show_animated_instructions() -> None:
    """Display animated game instructions"""
    console.clear()
    
    instructions_title = "📋 HOW TO PLAY"
    animated_text_display(f"\n{instructions_title}\n{'='*len(instructions_title)}\n", 
                         style="bold bright_magenta", delay=0.02)
    
    instructions = [
        "🎯 OBJECTIVE:",
        "   • Type the displayed text as quickly and accurately as possible",
        "   • Complete as many words as you can within the time limit",
        "",
        "🎮 CONTROLS:",
        "   • Just start typing! No need to click anywhere",
        "   • Use BACKSPACE to correct mistakes",
        "   • Press ESC to quit early",
        "",
        "📊 SCORING:",
        "   • WPM (Words Per Minute) = Your typing speed",
        "   • Accuracy = Percentage of correct characters",
        "   • Words Completed = Total words you finished",
        "",
        "🏆 DIFFICULTY LEVELS:",
        "   • 🟢 Beginner: Simple words (cat, dog, run)",
        "   • 🟡 Intermediate: Common phrases and sentences",
        "   • 🔴 Advanced: Complex sentences with punctuation",
        "",
        "💡 TIPS:",
        "   • Focus on accuracy first, speed will follow",
        "   • Use all your fingers, not just index fingers",
        "   • Keep your eyes on the screen, not the keyboard",
        "   • Take breaks to avoid strain",
        ""
    ]
    
    for line in instructions:
        if line.startswith("🎯") or line.startswith("🎮") or line.startswith("📊") or line.startswith("🏆") or line.startswith("💡"):
            animated_text_display(line + "\n", style="bold bright_cyan", delay=0.01)
        elif line.startswith("   •"):
            animated_text_display(line + "\n", style="bright_white", delay=0.005)
        else:
            animated_text_display(line + "\n", style="dim white", delay=0.005)
    
    animated_text_display("Press ENTER to continue...", style="bold bright_green blink", delay=0.03)
    input()

def show_scoreboard() -> None:
    """Display animated scoreboard"""
    console.clear()
    scores = load_scoreboard()
    
    # Animated title
    title = "🏆 HALL OF FAME 🏆"
    animated_text_display(f"\n{title}\n{'='*len(title)}\n", 
                         style="bold bright_yellow", delay=0.02)
    
    if not scores:
        animated_text_display("No scores yet! Be the first to set a record! 🌟\n", 
                             style="italic bright_yellow", delay=0.03)
    else:
        # Create animated table
        table = Table(show_header=True, header_style="bold bright_magenta", border_style="bright_blue")
        table.add_column("🥇 Rank", style="bold yellow", width=8)
        table.add_column("👤 Player", style="bold cyan", width=15)
        table.add_column("⚡ WPM", style="bold green", width=8)
        table.add_column("🎯 Accuracy", style="bold blue", width=10)
        table.add_column("📊 Level", style="bold magenta", width=12)
        table.add_column("📅 Date", style="dim white", width=16)
        
        for i, score in enumerate(scores[:10], 1):
            rank_emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}"
            table.add_row(
                rank_emoji,
                score["name"],
                f"{score['wpm']}",
                f"{score['accuracy']}%",
                score["difficulty"],
                score["date"]
            )
        
        console.print(table)
    
    animated_text_display("\nPress ENTER to return to menu...", 
                         style="bold bright_green", delay=0.02)
    input()

def show_menu_with_animation() -> None:
    """Display animated difficulty selection menu"""
    console.clear()
    
    # Animated menu title
    menu_title = "🎮 SELECT YOUR CHALLENGE"
    animated_text_display(f"\n{menu_title}\n{'='*len(menu_title)}\n", 
                         style="bold bright_cyan", delay=0.02)
    
    # Create animated menu options
    menu_options = [
        ("1", "🟢 BEGINNER", "Simple words and phrases", "Perfect for starters"),
        ("2", "🟡 INTERMEDIATE", "Common sentences", "Good challenge level"),
        ("3", "🔴 ADVANCED", "Complex text with punctuation", "For typing masters"),
        ("4", "🏆 SCOREBOARD", "View Hall of Fame", "See top performers"),
        ("5", "📋 INSTRUCTIONS", "How to play", "Learn the rules"),
        ("6", "🚪 EXIT", "Quit the game", "See you later!")
    ]
    
    table = Table(show_header=False, border_style="bright_blue", padding=(0, 1))
    table.add_column("Choice", style="bold yellow", width=8)
    table.add_column("Mode", style="bold cyan", width=20)
    table.add_column("Description", style="bright_white", width=25)
    table.add_column("Note", style="dim italic", width=20)
    
    for choice, mode, desc, note in menu_options:
        table.add_row(choice, mode, desc, note)
    
    console.print(table)

def get_words_by_difficulty(difficulty: int) -> List[str]:
    """Get words based on difficulty level"""
    if difficulty == 1:
        return beginner_words
    elif difficulty == 2:
        return intermediate_words
    else:
        return advanced_words

def render_text_with_transparency(target: str, typed: str, time_left: float, 
                                words_completed: int = 0, wpm: float = 0, 
                                accuracy: float = 0) -> Text:
    """Enhanced render with more stats"""
    stats_text = Text()
    stats_text.append("⏱️  TIME: ", style="bold bright_yellow")
    stats_text.append(f"{time_left:.0f}s", style="bold white")
    stats_text.append("  |  🏆 WORDS: ", style="bold bright_green")
    stats_text.append(f"{words_completed}", style="bold white")
    stats_text.append("  |  ⚡ WPM: ", style="bold bright_cyan")
    stats_text.append(f"{wpm:.1f}", style="bold white")
    stats_text.append("  |  🎯 ACC: ", style="bold bright_magenta")
    stats_text.append(f"{accuracy:.1f}%", style="bold white")
    
    # Progress bar for time
    time_bar = "█" * int((time_left / 60) * 30) + "░" * (30 - int((time_left / 60) * 30))
    stats_text.append(f"\n[{time_bar}]", style="bright_blue")
    
    # Text display
    text_display = Text("\n\n")
    for i, char in enumerate(target):
        if i < len(typed):
            if typed[i] == char:
                text_display.append(char, style="bold bright_green")
            else:
                text_display.append(char, style="bold white on red")
        elif i == len(typed):
            text_display.append(char, style="bold black on bright_white blink")
        else:
            text_display.append(char, style="dim white")
    
    # Instructions at bottom
    instructions = Text("\n\n💡 Keep typing! Press ESC to quit early.", style="dim bright_blue italic")
    
    return stats_text + text_display + instructions

class TypingGame:
    def __init__(self):
        self.typed: str = ""
        self.running: bool = False
        self.key_pressed: bool = False
    
    def on_key_event(self, event: keyboard.KeyboardEvent) -> None:
        """Handle keyboard events"""
        if not self.running:
            return
            
        if event.event_type == keyboard.KEY_DOWN:
            self.key_pressed = True
            if event.name == 'esc':
                self.running = False
            elif event.name == 'backspace':
                if self.typed:
                    self.typed = self.typed[:-1]
            elif event.name == 'space':
                self.typed += ' '
            elif len(event.name) == 1:
                self.typed += event.name

def play_game(difficulty: int, time_limit: int, player_name: str) -> None:
    """Enhanced game with better feedback"""
    words = get_words_by_difficulty(difficulty)
    target = random.choice(words).strip()
    
    game = TypingGame()
    game_started = False  # Track if user has started typing
    start_time: Optional[float] = None
    last_update_time: Optional[float] = None
    
    all_targets: List[str] = []
    all_typed: List[str] = []
    words_completed = 0
    wpm = 0.0
    accuracy = 100.0
    
    # Animated game start countdown
    console.clear()
    animated_text_display(f"🎯 Ready {player_name}? ", style="bold bright_cyan", delay=0.05)
    time.sleep(1)
    
    # Proper countdown: 3, 2, 1, GO!
    for i in range(3, 0, -1):
        console.clear()
        console.print(Text(f"{i}", style="bold bright_yellow", justify="center"))
        time.sleep(1)
    
    console.clear()
    console.print(Text("GO! ⚡", style="bold bright_green", justify="center"))
    time.sleep(0.5)
    console.clear()
    
    def get_time_left() -> float:
        nonlocal start_time
        if start_time is None:
            start_time = time.time()
        elapsed = time.time() - start_time
        return max(0, time_limit - elapsed)
    
    def calculate_stats() -> Tuple[float, float]:
        nonlocal wpm, accuracy, last_update_time, start_time
        now = time.time()
        if last_update_time is None or now - last_update_time > 0.3:
            if start_time is None:
                start_time = now
            elapsed = now - start_time
            if elapsed > 0:
                total_correct_chars = sum(1 for t, typed_text in zip(all_targets + [target], all_typed + [game.typed])
                                        for i in range(min(len(t), len(typed_text)))
                                        if i < len(typed_text) and typed_text[i] == t[i])
                total_chars = sum(len(typed_text) for typed_text in all_typed + [game.typed])
                
                wpm = (total_correct_chars / 5) / (elapsed / 60) if elapsed > 0 else 0
                accuracy = (total_correct_chars / total_chars) * 100 if total_chars > 0 else 100
            last_update_time = now
        return wpm, accuracy
    
    game.running = True
    keyboard.hook(game.on_key_event)
    
    try:
        with Live(render_text_with_transparency(target, game.typed, get_time_left(), 
                                              words_completed, wpm, accuracy), 
                  refresh_per_second=25, console=console) as live:
            
            while game.running:
                time_left = get_time_left()
                if time_left <= 0:
                    break
                
                current_wpm, current_accuracy = calculate_stats()
                live.update(render_text_with_transparency(target, game.typed, time_left, 
                                                        words_completed, current_wpm, current_accuracy))
                
                if game.typed == target:
                    all_targets.append(target)
                    all_typed.append(game.typed)
                    words_completed += 1
                    
                    # Show completion animation
                    completion_text = Text("✅ WORD COMPLETED! ", style="bold bright_green blink")
                    console.print(completion_text)
                    time.sleep(0.2)
                    
                    target = random.choice(words).strip()
                    game.typed = ""
                
                time.sleep(0.04)
    
    finally:
        keyboard.unhook_all()
        game.running = False
    
    if game.typed:
        all_targets.append(target)
        all_typed.append(game.typed)
    
    # Use actual start time for results calculation
    actual_start_time = start_time if start_time else time.time()
    show_results_with_animation(all_targets, all_typed, actual_start_time, time.time(), 
                               words_completed, player_name, difficulty, time_limit)

def show_results_with_animation(all_targets: List[str], all_typed: List[str], 
                               start_time: float, end_time: float, 
                               words_completed: int, player_name: str, 
                               difficulty: int, time_limit: int) -> None:
    """Enhanced animated results display"""
    console.clear()
    elapsed = end_time - start_time
    if elapsed <= 0:
        elapsed = 0.1
    
    # Calculate metrics
    total_chars_typed = sum(len(typed_text) for typed_text in all_typed)
    total_correct_chars = sum(1 for t, typed_text in zip(all_targets, all_typed) 
                            for i in range(min(len(t), len(typed_text)))
                            if i < len(typed_text) and typed_text[i] == t[i])
    total_target_chars = sum(len(target) for target in all_targets)
    
    wpm = (total_correct_chars / 5) / (elapsed / 60) if elapsed > 0 else 0
    raw_wpm = (total_chars_typed / 5) / (elapsed / 60) if elapsed > 0 else 0
    accuracy = (total_correct_chars / total_target_chars) * 100 if total_target_chars > 0 else 0
    
    # Animated results reveal
    animated_text_display("🎊 CALCULATING RESULTS... 🎊\n", style="bold bright_magenta", delay=0.05)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]Processing your performance..."),
        console=console,
    ) as progress:
        task = progress.add_task("", total=100)
        for i in range(100):
            progress.update(task, advance=1)
            time.sleep(0.02)
    
    console.clear()
    
    # Results title
    results_title = f"🏆 {player_name.upper()}'S PERFORMANCE REPORT 🏆"
    animated_text_display(f"\n{results_title}\n{'='*len(results_title)}\n", 
                         style="bold bright_yellow", delay=0.02)
    
    # Performance ratings
    wpm_rating = ("🚀 LIGHTNING FAST!" if wpm >= 70 else
                  "⚡ EXCELLENT!" if wpm >= 50 else
                  "👍 GOOD JOB!" if wpm >= 30 else
                  "📚 KEEP PRACTICING!" if wpm >= 15 else
                  "🐌 SLOW & STEADY!")
    
    acc_rating = ("🎯 PERFECT ACCURACY!" if accuracy >= 95 else
                  "✨ EXCELLENT PRECISION!" if accuracy >= 90 else
                  "👌 GOOD ACCURACY!" if accuracy >= 80 else
                  "📈 IMPROVING!" if accuracy >= 70 else
                  "🎯 FOCUS ON ACCURACY!")
    
    # Animated stats display
    stats = [
        ("⚡ NET WPM", f"{wpm:.1f}", wpm_rating),
        ("🏃 RAW WPM", f"{raw_wpm:.1f}", ""),
        ("🎯 ACCURACY", f"{accuracy:.1f}%", acc_rating),
        ("⏱️ TIME", f"{elapsed:.1f}s", ""),
        ("🏆 WORDS COMPLETED", f"{words_completed}", ""),
        ("✅ CORRECT CHARS", f"{total_correct_chars}", ""),
        ("📝 TOTAL CHARS", f"{total_chars_typed}", "")
    ]
    
    table = Table(show_header=True, header_style="bold bright_magenta", border_style="bright_green")
    table.add_column("📊 METRIC", style="bold cyan", width=20)
    table.add_column("📈 VALUE", style="bold white", width=15)
    table.add_column("🎯 RATING", style="bold yellow", width=25)
    
    for metric, value, rating in stats:
        table.add_row(metric, value, rating)
        time.sleep(0.3)  # Animated reveal
    
    console.print(table)
    
    # Save score and show message
    save_score(player_name, wpm, accuracy, difficulty, time_limit)
    
    # Performance message
    time.sleep(1)
    if wpm >= 50 and accuracy >= 90:
        animated_text_display(f"\n🌟 OUTSTANDING {player_name.upper()}! You're a typing wizard! 🧙‍♂️\n", 
                             style="bold bright_green", delay=0.03)
    elif wpm >= 30 or accuracy >= 80:
        animated_text_display(f"\n👏 WELL DONE {player_name.upper()}! Keep it up! 💪\n", 
                             style="bold bright_cyan", delay=0.03)
    else:
        animated_text_display(f"\n💪 GREAT EFFORT {player_name.upper()}! Practice makes perfect! 🎯\n", 
                             style="bold bright_blue", delay=0.03)
    
    animated_text_display("Your score has been saved to the Hall of Fame! 🏆\n", 
                         style="italic bright_yellow", delay=0.02)
    
    # Author credit
    animated_text_display("\n💻 Created by: Aditya | 🔗 GitHub: https://github.com/Adii0906\n", 
                         style="dim bright_blue", delay=0.01)
    
    animated_text_display("Press ENTER to continue...", style="bold bright_green", delay=0.02)
    input()

def main() -> None:
    """Enhanced main loop with animations"""
    greeting_shown = False
    
    while True:
        if not greeting_shown:
            show_animated_welcome()
            greeting_shown = True
        
        show_menu_with_animation()
        
        try:
            choice = Prompt.ask(
                "\n[bold bright_cyan]Choose your option[/bold bright_cyan]",
                choices=["1", "2", "3", "4", "5", "6"],
                default="1"
            )
            
            if choice == "4":  # Scoreboard
                show_scoreboard()
                continue
            elif choice == "5":  # Instructions
                show_animated_instructions()
                continue
            elif choice == "6":  # Exit
                animated_text_display("\n👋 Thanks for playing! Keep practicing! 🚀\n", 
                                     style="bold bright_green", delay=0.03)
                break
            
            # Get player info
            player_name = Prompt.ask("\n[bold bright_cyan]Enter your name[/bold bright_cyan]")
            console.print(f"\n[bold bright_green]👋 Welcome {player_name}![/bold bright_green]")
            
            difficulty = int(choice)
            time_limit = IntPrompt.ask(
                "\n[bold bright_yellow]⏰ Set time limit (seconds)[/bold bright_yellow]",
                default=60
            )
            
            play_game(difficulty, time_limit, player_name)
            
            play_again = Prompt.ask(
                f"\n[bold bright_cyan]🔄 Play again, {player_name}?[/bold bright_cyan]",
                choices=["y", "n"],
                default="y"
            )
            
            if play_again.lower() != 'y':
                animated_text_display(f"\n👋 Goodbye {player_name}! Thanks for playing! 🎮\n", 
                                     style="bold bright_green", delay=0.03)
                break
                
        except KeyboardInterrupt:
            animated_text_display("\n\n👋 Goodbye! See you next time! 🚀\n", 
                                 style="bold bright_red", delay=0.03)
            break
        except Exception as e:
            console.print(f"\n[bold red]❌ Error: {e}[/bold red]")
            time.sleep(2)

if __name__ == "__main__":
    main()