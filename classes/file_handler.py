from datetime import datetime
import json
import os
import sys
import pygame


class FileHandler:
    def __init__(self):
        self.portal_leaderboards_file_name = "portal_leaderboards.json"
        self.wall_leaderboards_file_name = "wall_leaderboards.json"
        self.leaderboards_folder_name = "leaderboards"
        self.wall_leaderboards_file_name = "wall_leaderboards.json"
        self.portal_leaderboards_path = os.path.join(
            self.leaderboards_folder_name, self.portal_leaderboards_file_name
        )
        self.wall_leaderboards_path = os.path.join(
            self.leaderboards_folder_name, self.wall_leaderboards_file_name
        )
        self.settings_file_name = "settings.json"

    # Reading related functions

    def paths_exists(self):
        if (
            not os.path.exists(self.portal_leaderboards_path)
            or not os.path.exists(self.wall_leaderboards_path)
            or not os.path.exists(self.settings_file_name)
        ):
            return False

        return True

    def read(self, path):
        try:
            with open(path, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            pygame.quit()
            sys.exit(f"An error has occured: {e}")

    def get_path(self, mode):
        if mode == "Portal":
            return self.portal_leaderboards_path
        return self.wall_leaderboards_path

    def get_data(self, mode):
        path = self.get_path(mode)
        return self.read(path)

    # Writing related functions

    def create_paths(self):
        try:
            if not os.path.exists(self.leaderboards_folder_name):
                os.makedirs(self.leaderboards_folder_name)
            if not os.path.exists(self.portal_leaderboards_path):
                with open(self.portal_leaderboards_path, "w", encoding="utf-8") as file:
                    data = []
                    json.dump(data, file)
            if not os.path.exists(self.wall_leaderboards_path):
                with open(self.wall_leaderboards_path, "w", encoding="utf-8") as file:
                    data = []
                    json.dump(data, file)
            if not os.path.exists(self.settings_file_name):
                with open(self.settings_file_name, "w", encoding="utf-8") as file:
                    data = [{"music_volume": 100, "sfx_volume": 100}]
                    json.dump(data, file, indent=4)
        except Exception as e:
            pygame.quit()
            sys.exit(f"An error has occured: {e}")

    def add_entry(self, mode, name, score):
        entry = {
            "name": name,
            "score": score,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        path = self.get_path(mode)
        data = self.read(path)
        data.append(entry)
        data.sort(key=lambda x: x["score"], reverse=True)
        data = data[:10]

        try:
            with open(path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            pygame.quit()
            sys.exit(f"An error has occured: {e}")

    def update_settings(self, audio_type, volume):
        settings = self.read(self.settings_file_name)

        if audio_type == "Music":
            settings[0]["music_volume"] = volume
        else:
            settings[0]["sfx_volume"] = volume

        try:
            with open(self.settings_file_name, "w", encoding="utf-8") as file:
                json.dump(settings, file, indent=4)
        except Exception as e:
            pygame.quit()
            sys.exit(f"An error has occured: {e}")
