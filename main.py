import customtkinter as ctk
from getpass import getuser
from essential_generators import DocumentGenerator
from difflib import SequenceMatcher

magic_generator = DocumentGenerator()
def get_random_sentence():
    return magic_generator.sentence()

class TypingSpeed(ctk.CTk):
    user = getuser()
    
    CPM_score = 0
    correctness_scores = []
    correctness_score = 0
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Typing Speed Test")
        self.geometry("800x400")
        self.grid_columnconfigure([i for i in range(8)], weight=1, uniform="yes")
        self.grid_rowconfigure([i for i in range(4)], weight=1, uniform="yes")     
        
        self.build_menu()
        
    def build_menu(self):
        self.text_label = ctk.CTkLabel(self, text=f"Welcome {self.user}", font=("Arial", 20))
        self.text_label.grid(row=0, column=3, columnspan=2, pady=2, sticky="news")
        
        self.start_button = ctk.CTkButton(self, text="Start", font=("Arial", 20), command=self.start)
        self.start_button.grid(row=1, column=3, columnspan=2, pady=2)
        
    def start(self):
        self.start_button.destroy()
        
        self.text_label.configure(text_color= "green")
        self.text_label.grid_configure(row=1, column=3, columnspan=2, pady=2, sticky="news")
        
        self.count_down(3)
        
    def count_down(self, count):
        if count > 0:
            self.text_label.configure(text=f"Good luck {self.user}!\n\n We are starting in {count} seconds")
            self.after(1000, self.count_down, count - 1)
        elif count == 0:
            self.text_label.configure(text="Let's type!", font=("Arial", 30))
            self.after(1000, self.start_test)
    
    def start_test(self):
        self.place_widgets_for_test()
        self.replace_sentence()
        self.reset_scores()
        
    def reset_scores(self):
        self.CPM_score = 0
        self.correctness_score = 0
        self.correctness_scores = []

    def replace_sentence(self):
        self.text_label.configure(text = f"{get_random_sentence()}")
        
    def place_widgets_for_test(self):
        self.text_label.grid_configure(row=0, rowspan=2, column=0, columnspan=8, ipadx=2, sticky="news")
        self.text_label.configure(font=("Arial", 26, "bold"), text_color="black", wraplength=800)

        self.input = ctk.CTkEntry(self, font=("Arial", 20), placeholder_text= "Start typing here", placeholder_text_color= "green")
        self.input.grid(row=2, column=1, columnspan=6, pady=2, sticky="news")
        self.input.focus_set()
        self.input.bind("<Key>", self.check_input)
        
        self.time_and_score_label = ctk.CTkLabel(self, text="Time remained: 60 seconds\n CPM: 0\nCorrectness: 0%", font=("Arial", 20))
        self.time_and_score_label.grid(row=3, column=2, columnspan=4, ipady=2, sticky="ew")
        
        self.after(1000, self.update_timer, 59)

    def update_timer(self, seconds):
        if seconds > 0:
            self.time_and_score_label.configure(text=f"Time remained: {seconds} seconds\n CPM: {self.CPM_score} \nCorrectness: {self.calculate_correctness(random_sentence= self.text_label.cget("text"), user_input= self.input.get())}%")
            self.after(1000, self.update_timer, seconds -1)
        elif seconds == 0:
            self.test_completed_show_report()
    
    def calculate_wpm(self):
        return round(self.CPM_score / 5.5)

    def calculate_correctness(self, random_sentence, user_input):
        self.correctness_score = round(SequenceMatcher(None, random_sentence[0:len(user_input)], user_input).ratio() * 100, 2)
        return self.correctness_score
            
    def check_input(self, event):
        self.CPM_score += 1
        if event.keysym == "Return" or len(self.input.get()) == len(self.text_label.cget("text")):
            self.replace_sentence()
            self.input.delete(0, "end")
            if len(self.input.get()) != 0:
                self.correctness_scores.append(self.correctness_score)
            else:
                self.correctness_scores.append(0)
        else:
            self.calculate_correctness(random_sentence= self.text_label.cget("text"), user_input= self.input.get())
    
    def test_completed_show_report(self):
        self.text_label.destroy()
        self.input.destroy()
        
        self.time_and_score_label.configure(text=f"Your WPM score (words per minute): {self.calculate_wpm()}\nYour CPM score (characters per minute) is {self.CPM_score}\n The average CPM is 200 and WPM is 40.\n\nCorrectness score is {self.calculate_final_correctness_score()}%")
        self.time_and_score_label.grid_configure(row=0, rowspan = 2, column=1, columnspan=6, pady=2, sticky="news")
        self.time_and_score_label.configure(font=("Arial", 26, "bold"), text_color="black", wraplength=800)
        
        self.restart_button = ctk.CTkButton(self, text="Restart?", font=("Arial", 20), command=self.restart)
        self.restart_button.grid(row=3, column=3, columnspan=2, pady=2)
    
    def calculate_final_correctness_score(self):
        return round(sum(self.correctness_scores) / len(self.correctness_scores), 2)
    
    def restart(self):
        self.restart_button.destroy()
        self.time_and_score_label.destroy()
        self.build_menu()
    
if __name__ == "__main__":
    TypingSpeed().mainloop()