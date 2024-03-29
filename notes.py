import pickle
from datetime import datetime, timedelta
from tag_manager import TagManager


class Note:
    def __init__(self, title, content, tags=None):
        self.title = title
        self.content = content
        self.tags = tags if tags else []
        self.created_at = datetime.now()

    def __str__(self):
        return f"{self.created_at}: {self.title} - {self.content} - Tagi: {', '.join(self.tags)}"


class Notebook:
    def __init__(self):
        self.notes = []
        self.tag_manager = TagManager(self.notes)  # Adding TagManager

    def add_note(self, title, content, tags=None):
        tags = tags or []  # Ustaw pustą listę, jeśli tags jest None
        note = {"title": title, "content": content, "tags": tags}
        self.notes.append(note)
        self.update_tags()

    def update_tags(self):
        self.tag_manager.set_notes(self.notes)

    def show_notes(self):
        if not self.notes:
            print("Brak notatek do wyświetlenia.")
            return
        for idx, note in enumerate(self.notes, start=1):
            print(f"""ID: {idx} Tytuł: {note.get('title', 'Brak tytułu')}
    Treść: {note.get('content', 'Brak treści')}
    Tagi: {', '.join(note.get('tags', []))}""")

    def delete_note(self, note_id):
        try:
            note_id = int(note_id)
            if 0 < note_id <= len(self.notes):
                deleted_note = self.notes.pop(note_id - 1)
                print(f"Usunięto notatkę: {
                      deleted_note.get('title', 'Brak tytułu')}")
            else:
                print("Notatka o podanym ID nie istnieje.")
        except ValueError:
            print("Podane ID nie jest liczbą całkowitą.")
        except IndexError:
            print("Podane ID jest poza zakresem listy notatek.")

    def edit_note(self):
        if not self.notes:
            print("Brak notatek do wyświetlenia.")
            return

        self.show_notes()
        note_id_input = input("Podaj ID notatki do edycji: ")

        try:
            note_id = int(note_id_input) - 1
            if note_id < 0 or note_id >= len(self.notes):
                print("Niepoprawne ID notatki.")
                return
        except ValueError:
            print("Nieprawidłowa wartość ID. Proszę podać liczbę.")
            return

        note = self.notes[note_id]
        title = input(
            "Podaj nowy tytuł notatki (naciśnij Enter, aby pominąć): ")
        content = input(
            "Podaj nową treść notatki (naciśnij Enter, aby pominąć): ")
        tags_input = input(
            "Podaj nowe tagi oddzielone przecinkami (lub wciśnij Enter, aby pominąć): ")
        tags = [tag.strip() for tag in tags_input.split(",")
                ] if tags_input else note['tags']

        # Aktualizacja notatki
        note['title'] = title if title else note['title']
        note['content'] = content if content else note['content']
        note['tags'] = tags

        print("Notatka została zaktualizowana.")

    def update_note(self, note_id, title=None, content=None, tags=None):
        """Aktualizuje notatkę o podanym ID."""
        note = self.notes[note_id]
        if title:
            note['title'] = title
        if content:
            note['content'] = content
        if tags is not None:
            note['tags'] = tags

        print("Notatka została zaktualizowana.")

        print("Notatka została zaktualizowana.")

    def search_notes_by_tag(self, tag):
        found_notes = [note for note in self.notes if tag in note['tags']]
        if not found_notes:
            print("Nie znaleziono notatek z podanym tagiem.")
        else:
            for note in found_notes:
                print(f"Tytuł: {note['title']}\nTreść: {
                      note['content']}\nTagi: {', '.join(note['tags'])}")

    def save_notes(self, filename='notes.pkl'):
        try:
            with open(filename, 'wb') as file:
                pickle.dump(self.notes, file)
            print("Notatki zostały zapisane.")
        except Exception as e:
            print(f"Błąd przy zapisie notatek: {e}")

    def load_notes(self, filename='notes.pkl'):
        try:
            with open(filename, 'rb') as file:
                self.notes = pickle.load(file)
            print("Notatki zostały wczytane.")
        except FileNotFoundError:
            print("Plik z notatkami nie istnieje. Tworzenie nowego pliku.")
            self.notes = []
        except Exception as e:
            print(f"Błąd przy wczytywaniu notatek: {e}")

    def sort_notes_by_tags(self, tag):
        """Sortuje notatki według daty utworzenia dla wybranego tagu."""
        notes_with_tag = [note for note in self.notes if tag in note['tags']]
        if not notes_with_tag:
            print("Brak notatek z podanym tagiem.")
            return False  # Wskazuje na to, że sortowanie nie zostało wykonane

        sorted_notes = sorted(notes_with_tag, key=lambda x: x.get(
            'created_at', datetime.min), reverse=True)
        self.notes = sorted_notes + \
            [note for note in self.notes if note not in notes_with_tag]
        return True

    def show_unique_tags(self):
        unique_tags = set()
        for note in self.notes:
            for tag in note['tags']:
                unique_tags.add(tag)
        print("Dostępne tagi:", ", ".join(unique_tags)
              if unique_tags else "Brak tagów")
