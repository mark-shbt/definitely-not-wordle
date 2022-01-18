from random_word import RandomWords
from typing import Union
from datetime import datetime
import pyperclip

TRIES = 6
rand_word = RandomWords()
DIVIDER = '=' * 15
KEYBOARD = '''
.-----.-----.-----.-----.-----.-----.-----.-----.-----.-----.
|  Q  |  W  |  E  |  R  |  T  |  Y  |  U  |  I  |  O  |  P  |
|  q  |  w  |  e  |  r  |  t  |  y  |  u  |  i  |  o  |  p  |
.-----.-----.-----.-----.-----.-----.-----.-----.-----.-----.
 |  A  |  S  |  D  |  F  |  G  |  H  |  J  |  K  |  L  |
 |  a  |  s  |  d  |  f  |  g  |  h  |  j  |  k  |  l  |
 .-----.-----.-----.-----.-----.-----.-----.-----.-----.
     |  Z  |  X  |  C  |  V  |  B  |  N  |  M  |
     |  z  |  x  |  c  |  v  |  b  |  n  |  m  |
     .-----.-----.-----.-----.-----.-----.-----.
'''
SUCCESS = ':large_green_square:'
MAYBE = ':large_yellow_square:'
OFF = ':white_large_square:'

def updated_keyboard(keyboard: str, p_words: list, q_words: list, w_words: list) -> str:
	for word in p_words:
		index = KEYBOARD.index(word)
		if keyboard[index] != '+':
			keyboard = keyboard[:index] + '+' + keyboard[index + 1:]
	for word in q_words:
		index = KEYBOARD.index(word)
		if keyboard[index] == '+':
			continue
		keyboard = keyboard[:index] + '?' + keyboard[index + 1:]
	for word in w_words:
		keyboard = keyboard.replace(word, '-')
	return keyboard

def check_user_guess(guess: str, word: str, keyboard: str) -> Union[str, str, str, bool, str]:
	'''
	check user's guess vs the actual word
	return 2 str + bool to show if the guess is correct
		- first is the word formatted
		- other is showing which words are guessed right
	return: formatted_guess, formatted_hints, emoji_results, guess_correct, keyboard
	ex:
		word:  angle
		guess: about
		ret: [a][b][o][u][t]
			 	 [+][-][-][-][-]

		word:  table
		guess: swear
		ret: [s][w][e][a][r]
			 	 [-][-][?][-][-]
	'''
	results = guess == word
	formatted_guess = ''
	formatted_hints = ''
	p_words = []
	q_words = []
	w_words = []
	emoji_results = ''

	for index in range(len(guess)):
		if guess[index] == word[index]:
			formatted_hints += '[+]'
			emoji_results += SUCCESS
			p_words.append(guess[index])
		elif guess[index] in word:
			formatted_hints += '[?]'
			emoji_results += MAYBE
			q_words.append(guess[index])
		elif guess[index] != word[index]:
			formatted_hints += '[-]'
			emoji_results += OFF
			w_words.append(guess[index])
		formatted_guess += f'[{guess[index]}]'

	
	return formatted_guess, formatted_hints, emoji_results, results, updated_keyboard(keyboard, p_words, q_words, w_words)

def update_history(history, guess, hint):
	history.append(guess)
	history.append(hint)
	history.append(DIVIDER)

def get_time(timedelta):
	sec = f'{timedelta.seconds % 60} sec'
	min = f'{timedelta.seconds // 60} min, '
	
	return min + sec
	

def play():
	user_input = ''
	to_continue = 'y'
	guess_correct = False

	intro = '''
	Welcome to Definitely Not Wordle!
	Rules:
	- The program will randomly generate a 5-letter word
	- You have 6 chances to guess the word
	- After each guess, there'll be a  keyboard with '+', '?', '-' printed out
		- '+' means the letter you guessed is at the right place (there could be repeating letters per word!)
		- '?' means the letter you guessed is in the word but it's not at the right place
		- '-' means the letter you guessed isn't in the word
	- After finishing the round, the program will copy the results to your clipboard so you can just paste them into the slack channel if you'd like :)
		- If it isn't copied to your clipboard you can still copy the results manually to share

	Press anykey to continue
	'''
	dummy = input(intro + '\n')


	while to_continue.lower() == 'y':
		user_tries = 0
		guess_correct = False
		keyboard = KEYBOARD
		print('Your mystery word is now generating...')
		generated_word = rand_word.get_random_word(hasDictionaryDef='true', includePartOfSpeech="noun,verb,adjective,adverb", minLength=5, maxLength=5)
		while not generated_word or not generated_word.isalpha():
			generated_word = rand_word.get_random_word(hasDictionaryDef='true', includePartOfSpeech="noun,verb,adjective,adverb", minLength=5, maxLength=5)
		generated_word = generated_word.lower()
		history = ['====HISTORY====', 'Word: ' + generated_word]
		progress = []
		emoji_results = ''
		
		print('Guess the wordle!')
		start_time = datetime.now()
		while user_tries < TRIES and not guess_correct:
			while len(user_input) != 5:
				print(f'Remaining tries: {TRIES - user_tries}')
				user_input = input('> ')
				if len(user_input) != 5:
					print('Please enter words with 5 characters only')
			formatted_guess, formatted_hints, emotes, guess_correct, keyboard = check_user_guess(user_input, generated_word, keyboard)
			emoji_results += emotes + '\n'
			user_input = ''
			print(formatted_guess)
			print(formatted_hints)
			print(keyboard)
			update_history(progress, formatted_guess, formatted_hints)
			user_tries += 1
		
		end_time = datetime.now()
		time_took = get_time(end_time - start_time)
		
		if guess_correct:
			print(f'\nCograts! You guessed the word in {time_took} :)')
		else:
			print('\nMaybe you\'ll get it next time :)')
		history[1] += f'  |  {user_tries} / {TRIES}'
		for item in history:
			print(item)
		print(keyboard)

		copy_cb = f'Wordle  - {generated_word}  |  {time_took}  |  {user_tries} / {TRIES}\n\n' + emoji_results
		try:
			pyperclip.copy(copy_cb)
		except:
			pass
		print(copy_cb)

		to_continue = input('\nDo you want to continue? Enter \'y\' to continue. Otherwise, enter any character to exit the program: ')
	
if __name__ == '__main__':
	play()