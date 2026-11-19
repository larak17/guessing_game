# Hangman

For this project we decided to implement the guessing game Hangman. We decided to use an LLM to generate the hidden word. To guess the word, we implemented two different approaches: the individual letter in the format of buttons and a chat input, where the whole word can be typed in. Each input counts as one individual guess, therefore guessing the word as a whole only counts as one guess. If a wrong input is given, it will be counted as an error. Each error is illustrated by a new line of the hangman that is shown on the left side of the page. It is possibe to guess up until 10 errors, then the game is finished either way. 
To keep track of the data that is produced during the game, we decided to create a new json file for each game where the word lenght, the overall guesses taken and the wrong guesses (errors) are saved. This json file can then be used to create the statistics on the stats page. There one can see how many games the player won, or lost. Also the average number of guesses and average number of erros can be observed. Moreover, a bar plot shows how many guesses were needed in each game, as well as the proportion of wrong guesses (errors) within the overall guesses. 

A short timeline of the project: 

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

(18.11) we:
- put more interesting statistics on the stats page (maybe still change some)
- designed the main page
- put hangman on the sidebar
- included chat component to guess whole word
- only have one json file per player so that stats are only for the person that plays at the moment (gets deleted afterwards)
- make sure generated words are not used twice in the same game (put into a list)

(19.11) we:
- added a second button to directly view the stats page
- cleaned up the code and repository a bit
- started writing an overview for the project
- added an information on the stats page that one needs to play a game to see statistics (to not have an error message)
