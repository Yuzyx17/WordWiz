import pygame as pg

from src.core.state import BoardState
from src.core.letters import Letter
from src.game.player import Player
from src.utils.button import Button
from src.utils.generator import LetterGenerator
from src.game.ai import AI
from src.constants import *
from src.utils.text import TextRenderer

# ADD HERE
from src.utils.text import TextRenderer

class Board():
    def __init__(self, canvas):
        self.state = BoardState()
        self.canvas = canvas
        self.spell = False   #if player is allowed to spell
        self.click = False   #for detecting clicks; communicates from events
        self.cont = False
        self.start_game = False
        self.pool = ""

        self.player = Player(self)
        self.ai = AI(self)
        self.pool_generator = LetterGenerator(self.state.trie)

        self.time = 0
        self.round = 1
        self.phase = 0
        self.max_round = 3

        self.text_group = pg.sprite.Group()
        #MASTERMIND ALWAYS STARTS FIRST
        self.turn = False #True = Player; False = AI
        self.mode = False #True = CB; False = MM #DEFAULT FALSE
         
        self.letter_pool = pg.sprite.Group()
        self.letter_used = pg.sprite.Group()
        self.letter_hints = pg.sprite.Group()
        self.word_guessed = pg.sprite.Group()
        self.correct_word = pg.sprite.Group()
        self.buttons = pg.sprite.Group()
        
        self.player_role = TextRenderer(vec2(100, 70))
        self.player_role.rect.topleft = vec2(SIZE.x - self.player_role.rect.w -20, 0)
    
        self.round_text = TextRenderer(vec2(100, 50))
        self.round_text.rect.topleft = vec2(500, 50)
        self.round_text.change_text(f"Round: {self.round}")

        self.scores = TextRenderer(vec2(100, 100))
        self.scores.rect.topleft = vec2(500, 50)

        self.wl = TextRenderer(vec2(350, 100))
        self.wl.change_text("Your role in first round?")
        self.wl.rect.topleft = vec2(145, 340)
        self.text_group.add(self.wl)

        self.gen = Button(vec2(150, 75), pg.Color(100, 150, 175))
        self.gen.on_click(self.guess)
        self.gen.set_text("")
        self.gen.rect.topleft = vec2(375, 200)

        self.start_init()

    # STOP HERE
    # if cb, then 
    def start_init(self):
        self.buttons.empty()
        self.text_group.empty()
        text = TextRenderer(vec2(350, 100))
        text.change_text("Your role in first round?")
        text.rect.topleft = vec2(145, 100)
        self.text_group.add(text)

        cb_button = Button(vec2(150, 50), pg.Color(116,216,26))
        cb_button.on_click(self.on_cb)
        cb_button.set_text("Codebreaker")
        cb_button.rect.topleft = vec2(100, 250)
        self.buttons.add(cb_button)

        mm_button = Button(vec2(150, 50), pg.Color(220,53,69))
        mm_button.on_click(self.on_mm)
        mm_button.set_text("Mastermind")
        mm_button.rect.topleft = vec2(400, 250)
        self.buttons.add(mm_button)

    def restart(self):
        self.start_game = False
        self.round = 0
        self.ai.score = 0
        self.player.score = 0
        self.start_init()
        text = ""
        if self.ai.score > self.player.score:
            text = f"AI WIN"
        elif self.ai.score < self.player.score:
            text = f"PLAYER WIN"
        else:
            text = "DRAW"
        self.wl.change_text(f"{text}")
        self.text_group.add(self.wl)
        

    def game_init(self):
        self.buttons.empty()
        self.text_group.empty()
        self.start_game = True
        

        res = Button(vec2(150, 75), pg.Color(250, 100, 125))
        res.on_click(self.player.giveup)
        res.set_text("Give Up")
        res.rect.topleft = vec2(375, 300)

        self.buttons.add(self.gen)
        self.buttons.add(res)
        self.text_init()

    def on_mm(self):
        self.change_turn(turns.PMM)
        self.game_init()
        self.pl_mm_init()
        

    def on_cb(self):
        self.change_turn(turns.PCB)
        self.game_init()
        self.ai_mm_init()

    def render_hints(self):
        word = self.state.wordify_guess(self.state.attempt-1)
        for index in range(len(word)):
            char = word[index]
            letter = Letter(char)
            letter.rect.topleft = vec2(tilesize.x*index, 100+((self.state.attempt-1)*tilesize.y))
            letter.fill = WHITE
            if self.state.hints[index] == char:
                letter.fill = GREEN
            letter.draw()
            self.word_guessed.add(letter)

    def text_init(self):
        self.text_group.add(self.player_role)
        self.text_group.add(self.scores)
        self.text_group.add(self.round_text)

    #for each round
    def update_turn(self, pool = None):
        self.word_guessed.empty()
        self.letter_pool.empty()
        self.letter_used.empty()
        self.letter_hints.empty()
        self.state.reset()
        if pool == None: return
        if len(pool) != 10:
            return
        self.pool = pool

        if not self.turn:
            self.ai.cb_init(self.pool)

        self.state.pool_string = pool
        for i in range(10):
            self.state.pool[i] = self.pool[i]
            letter = Letter(self.state.pool[i])
            letter.rect.x = i*tilesize.x
            self.letter_pool.add(letter)

    #for each turn
    def reset_pool(self):
        self.render_hints()

        self.letter_pool.empty()
        self.letter_used.empty()
        self.letter_hints.empty()

        for i in range(10):
            self.state.pool[i] = self.pool[i]
            letter = Letter(self.state.pool[i])
            letter.rect.x = i*tilesize.x
            self.letter_pool.add(letter)

    def draw(self):
        self.text_group.draw(self.canvas)
        self.buttons.draw(self.canvas)
        self.text_group.update()
        self.buttons.update(self.click)

        if self.start_game:
            self.word_guessed.draw(self.canvas)     #drawing guesses
            self.letter_pool.draw(self.canvas)      #drawing pool of letters
            self.letter_used.draw(self.canvas)      #drawing spell attempt
            self.letter_hints.draw(self.canvas)
            self.correct_word.draw(self.canvas)


            self.letter_pool.update()
            self.letter_used.update()
            self.letter_hints.update()
            self.correct_word.update()
            
            if self.phase == 4:
                self.phase = 0
                self.round += 1
                self.round_text.change_text(f'Round: {self.round}')

            if not self.turn and not self.mode:          
                pass            
            elif self.turn and self.mode:                                       
                self.player.codebreaker()           
            elif self.turn and not self.mode:        
                self.player.mastermind()            
            elif not self.turn and self.mode and self.time % self.ai.speed == 0 :    
                self.time = 0                                   
                self.ai.codebreaker()        

            #TEMPORARY FEEDBACK
            
            self.color_feedback()
            self.update()
            self.time += 1
            if self.time % 1000 == 0:
                self.time = 0

    def color_feedback(self):
        letter : Letter
        if self.state.verify_guess() and self.mode:
            for letter in self.letter_used:
                letter.fill = GREEN
                letter.draw()
        elif self.state.verify_code() and not self.mode:
            for letter in self.letter_used:
                letter.fill = GREEN
                letter.draw()
        else:
            for letter in self.letter_used:
                letter.fill = RED
                letter.draw()
        
        for letter in self.letter_pool:
            if letter not in self.letter_used:
                letter.fill = WHITE
                letter.draw()
            if letter in self.letter_hints and letter in self.letter_used:
                index = self.state.guesses[self.state.attempt].index({self.letter_pool.sprites().index(letter): letter.letter})
                if self.state.hints[index]:
                    if self.state.hints[index] == letter.letter:
                        letter.fill = GREEN 
                        letter.draw()

        for letter in self.correct_word.sprites():
            letter.fill = GREEN
            letter.draw()

    def ai_mm_init(self):
        self.ai.mastermind()

        #self.update_turn(self.pool)
        #self.ai.mastemrind(self.pool)
        self.correct_word.empty()
        self.ai.word = self.ai.agent_mastermind.generateWord()
        self.pool_generator.mmWord = [letter for letter in self.ai.word]
        self.pool = None
        self.pool_generator.min = AI_WORD_POOL_DIFFICULTY
        self.pool_generator.limit = 150
        while self.pool == None:
            generated = self.pool_generator.letter_generate()
            if generated:
                self.pool = ''.join(generated['pool'])
                del generated
        self.update_turn(self.pool)
        self.change_turn(turns.PCB)
        self.state.code_string = self.ai.word
        self.phase += 1

    def pl_mm_init(self):
        #PLAYER MASTERMIND
        if self.state.accept_code():
            self.pool_generator.mmWord = [letter for letter in self.state.code_string]
            self.pool = None
            self.pool_generator.min = PLAYER_POOL_DIFFICULTY
            self.pool_generator.limit = 5000
            while self.pool == None:
                generated = self.pool_generator.letter_generate()
                if generated:
                    self.pool = ''.join(generated['pool'])
                    del generated
            self.update_turn(self.pool)

            #self.reset_pool()
            self.change_turn(turns.ACB)
            self.state.code_string = ''.join(self.player.word)
            self.phase += 1
            self.ai.cb_init(self.pool)   
            self.correct_word.empty()

    def guess(self): #This is attached to the button in wordwiz.py as a callback
        if self.round == self.max_round:
            self.restart()
        if not self.turn and not self.mode:
            self.ai_mm_init()
        if self.turn and self.mode:
            if self.state.accept_guess():
                self.reset_pool()
                self.player.get_hints()
        if self.turn and not self.mode:
            self.pl_mm_init()
        if not self.turn and self.mode:
            ...

    def display_correct_word(self):
        for i in range(len(self.state.code_string)):
            letter = Letter(self.state.code_string[i])
            letter.rect.x = i*tilesize.x
            letter.rect.y = SIZE.y - tilesize.y
            self.correct_word.add(letter)

    def update(self):
        ...

    def change_turn(self, turn: turns):
        self.scores.change_text(f'Player: {self.player.score}\nAI: {self.ai.score}')
        match turn:
            case turns.PCB:
                self.turn = True
                self.mode = True
                self.player_role.change_text(f"Player\nCodebreaker")
                self.gen.change_text("GUESS!")
            case turns.PMM:
                self.turn = True
                self.mode = False
                self.player_role.change_text(f"Player\nMastermind")
                self.gen.change_text("SET WORD")
            case turns.ACB:
                self.turn = False
                self.mode = True
                self.player_role.change_text(f"AI\nCodebreaker")
                self.gen.change_text("CONTINUE")
            case turns.AMM:
                self.turn = False
                self.mode = False
                self.player_role.change_text(f"AI\nMastermind")
                self.gen.change_text("CONTINUE")
            case other:
                raise("ERROR AWIT")

    def events(self, event):
        if self.turn and not self.mode:
            if event.type == pg.KEYDOWN:
                if event.unicode.isalpha():
                    if self.spell:
                        self.state.spell_code(len(self.player.word), event.unicode)
                        self.player.word.append(event.unicode)
                        letter = Letter(event.unicode)
                        letter.rect.x = len(self.player.word)*tilesize.x
                        self.letter_used.add(letter)
                        print(self.state.code)
                elif event.key == pg.K_BACKSPACE:
                    if len(self.player.word) > 0:
                        self.state.code[len(self.player.word)-1] = ' '
                        self.letter_used.remove(self.letter_used.sprites()[-1])
                        self.player.word.pop()
                        print(self.state.code)