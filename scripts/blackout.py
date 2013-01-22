# Author: Abid H. Mujtaba
# Date: Jan. 21, 2012

# This file implements the Blackout class which can be considered the Kernel of the Blackout web-application (being implemented using Django). The purpose of the class is to implement an entire game of Blackout in an abstract fashion which can then be interfaced using the designed class API to play the game either by a terminal or the internet via a web server.

# In conjunction with the Blackout class we construct a number of classes to represent card suits, ranks and the cards themselves. These classes implement a lot of the precedence functionality of the cards including trump and which suit was led in a hand which will simplify the logic and implementation of the actual Blackout class


from cards import *		# Access all the playing card implementing classes and enumerations from the cards module (custom-built)


class Blackout :

	'''
	This is the primary class that implements the game: Blackout. This is meant to be an abstract implementation with an API designed to be accessed by other Python objects and functions which will in turn implement the interface (either terminal or web-based or whatever other way one deems fit).

	The game 'Blackout' also known as 'Oh, Hell' is explained in http://en.wikipedia.org/wiki/Blackout_(card_game).

	The variant of the game we will be working with has the following unique rules:

	(a) The first round has one trick.

	(b) At each round the number of tricks increases by one until it reaches seven (this number will be the default but will be changeable).

	(c) For subsequent rounds the number of tricks decreases by one until only one trick is left which constitutes the last round.

	(d) The dealer is forced to bid such that the total number of bids is NOT equal to the number of tricks in that round.

	(e) The dealer is chosen randomly to begin with and then the dealer position moves left every round.

	(f) You get 10 points for making your bid and one point for each trick you take regardless of whether you bid or not.
	'''

	def __init__( self, numPlayers, maxTricks = 7 ) :

		'''
		Class constructor. Every instance of the game must of course know the number of players.

		The maxTricks value with default value of 7 is the max. no. of tricks the game increases up to before decreasing again. The constructor will check whether the value passed is feasible.
		'''

		assert 0 < maxTricks < 14, 'ERROR: maxTricks must be an integer between 1 and 13'


		if numPlayers * maxTricks > 52 :		# The number of players and maxTricks is so high that the deck doesn't contain enough cards to go on

			# We must decrease maxTricks so that the game can be played with a single deck

			maxTricks = 52 / numPlayers		# Integer division


		self.numPlayers = numPlayers
		self.maxTricks = maxTricks

		self.Round = 1		# Declare it to be the first round

		self.Dealer = 0		# Player 0 will be the dealer

		self.numTricks = 1		# There will be 1 trick in the first round

		# We now create the deck by constructing a list of Card objects stored in a list so that each card in the deck is associated with a unique integer from 0 to 51:

		self.Deck = []

		for suit in [ Suit.Spade, Suit.Heart, Suit.Club, Suit.Diamond ] :

			for rank in [ Rank.Two, Rank.Three, Rank.Four, Rank.Five, Rank.Six, Rank.Seven, Rank.Eight, Rank.Nine, Rank.Ten, Rank.Jack, Rank.Queen, Rank.King, Rank.Ace ] :

				self.Deck.append( Card( suit, rank ) )		# create and append card object to self.Deck


		# Prepare a data structure to store player information:

		self.Player = []

		for ii in range( numPlayers ) :

			self.Player.append( { 'hand': [] } )		# Give each player a dictionary containing a 'hand' key with an empty list to store integers representing cards in their hands




	def _dump( self ) :

		'''
		Internal method for dumping the state of the Blackout object to help debug the code.
		'''
		
		print
		print( "self.numPlayers = %d" % self.numPlayers )
		print( "self.maxTricks = %d" % self.maxTricks )
		print( "Round = %d" % self.Round )
		print( "Dealer = %d" % self.Dealer )
		print( "self.numTricks = %d" % self.numTricks )
#		print
#		print( "Deck : " + str( self.Deck ) )
		print
		print( "Player Data :- " )
		print

		for ii in range( self.numPlayers ) :

			print( '     Player %d : %s' % (ii, self.Player[ii] ) )

	
	def _circInc( self, num ) :

		'''
		Increments 'num' by 1 and rotates it around to zero if the new numbers equals (or exceeds) self.maxPlayers.

		Used internally to increment the player number.
		'''

		return (num + 1) % self.numPlayers


	


	def nextDeal( self ) :

		'''
		This method implements the cards being dealt for the next round.
		'''

		# The first step is to shuffle the deck.

		from random import shuffle

		shuffled = range(51)		# list of 52 integers starting at zero

		shuffle( shuffled )		# self.shuffled will contain a list of integers that point to cards in self.Deck

		
		# Now we clear the round variables in self for the next round:

		self.clearRound()


		# Now we populate the player hands remembering that we must keep track of the dealer and start dealing to the player with the higher integer (modelled to be the one to the left of the dealer).

		index = 0

		for trick in range( self.numTricks ) :		# No. of cards to be dealt out to each player

			for player in circGen( self.Dealer + 1, self.numPlayers ) :

				self.Player[ player ][ 'hand' ].append( self.Deck[ shuffled[ index ] ] )

				index += 1


		# The next card from the deck will determine the trump:

		self.TrumpCard = self.Deck[ shuffled[ index ] ]

		
		# Store the trump based on the TrumpCard dealt:

		self.trump = self.TrumpCard.Suit

		self.trump.trump = True			# Tell the trump suit that it has been declared trump

			


	

	def clearRound( self ) :

		'''
		This method is intended to be called after each round is played. It is used to clear and prepare anew the various variables that are used within each round. It prepares these variables/members for the next round.
		'''
		
		# Clear the trump and led suit indicators

		self.trump.trump = False
		self.led.led = False

		# Clear the player hands

		for ii in range( self.numPlayers ) :

			self.Player[ii][ 'hand' ] = []		# Clear the lists to indicate empty hands for each player


		# Advance the dealer:

		self.Dealer = self._circInc( self.Dealer )


		# Advance the round number:

		self.Round += 1
		

		# Advance the number of tricks

		if self.Round > self.maxTricks :		# The new Round number is greater than the max no. of tricks (globally) allowed and so we are in the decreasing trick phase of the game

			self.numTrikcs -= 1

		else :
			
			self.numTricks += 1





def circGen( total, start ) :

	'''
	This is a generator which creates a sequence of integers starting with the value 'start' which goes up to 'total - 1' and then circles back around to begin from zero. A single iteration is created.
	'''

	assert start > -1, 'ERROR: start must be a positive integer preferably between 0 and (total - 1)'


	start = start % total		# We allow for the fact that start might be outside of total already


	for ii in range(total) :

		yield (ii + start) % total
