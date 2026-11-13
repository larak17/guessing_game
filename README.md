# guessing_game

(03.11) we:

- created two pages, one for the game and one for the stats 
- in page1: instructions + underscore for each letter in word + displaying keyboard of letters

(06.11) we:

- disabled buttons (letters) that are pressed
- checked each pressed button (letter) against the word and display the output

(11.11) we:
- integraded the LLM to generate words for the game
- use the generated word to check the input against
- create the hangman illustration and integrate it into the code
- manage that a new word gets generated when 'start' is pressed
- have a max of 10 wrong guesses (illustrated by the hangman) and end the game when reached

(13.11) we:
- included a function that safes the information needed for the stats page in a json file after a game if lost or won -> including information about the game number, the overall guesses, the wrong guesses and correct guesses. More information can also be included there
- first bar plot on the stats page where just Games vs. Numer of Guesses are displayed -> we can either make more plots with different information or also assess here the quality of the guesses
