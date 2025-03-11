from flask import Flask, render_template, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = "HanGgAme_DesIgnEbYSanKetdEveLopeR"  

# Word list
WORDS = ["ferrari", "bugatti", "mercedes", "porsche", "mclaren", "rollsroyce","tesla","audi","lamborghini"]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Start a new game
        session["word"] = random.choice(WORDS)
        session["guessed_letters"] = []
        session["incorrect_guesses"] = 0
        return redirect("/game")
    return render_template("index.html")

@app.route("/game", methods=["GET", "POST"])
def game():
    if "word" not in session:  # jar game active nasel tar home page vr redirect hotay
        return redirect("/")
    
    word = session["word"]
    guessed_letters = session["guessed_letters"]
    incorrect_guesses = session["incorrect_guesses"]

    if request.method == "POST":
        guess = request.form.get("guess", "").lower()

        # Validate input
        if len(guess) != 1 or not guess.isalpha():
            return render_template("game.html", error="Please enter a single valid letter.")
        if guess in guessed_letters:
            return render_template("game.html", error="You've already guessed that letter.")

        #  guess la process kartay
        guessed_letters.append(guess)
        session["guessed_letters"] = guessed_letters
        if guess not in word:
            session["incorrect_guesses"] += 1

    #  win/lose conditions baghtay
    revealed_word = " ".join([letter if letter in guessed_letters else "_" for letter in word])
    if all(letter in guessed_letters for letter in word):
        return render_template("game.html", win=True, word=word)
    if session["incorrect_guesses"] >= 6:
        return render_template("game.html", lose=True, word=word)

    #  game page vr render kartay
    return render_template(
        "game.html",
        word=revealed_word,
        guessed_letters=", ".join(sorted(guessed_letters)),
        lives_remaining=6 - session["incorrect_guesses"],
        hangman_stage=session["incorrect_guesses"]
    )

if __name__ == "__main__":
    app.run(port=8000)