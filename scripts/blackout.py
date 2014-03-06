# Copyright 2013 Abid Hasan Mujtaba
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Author: Abid H. Mujtaba
# Date: Jan. 21, 2013

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

		self.Bidder = 1		# Player #1 will be the first one to bid.

		self.Current = 1		# Player #1 will be the first one to have a turn

		self.Leader = 1			# Player #1 will lead in this round.

		self.numTricks = 1		# There will be 1 trick in the first round


		self.currentTrick = list( range( self.numPlayers ) )		# Create a list which will store the cards each player plays in a single trick
		self.currentTrick[0] = None		# Store None for Leader
		self.currentTrick[-1] = None		# Store None for player before dealer. Used by evalTrick to check validity of hand played


		# We now create the deck by constructing a list of Card objects stored in a list so that each card in the deck is associated with a unique integer from 0 to 51:

		self.Deck = []

		for suit in [ Suit.Spade, Suit.Heart, Suit.Club, Suit.Diamond ] :

			for rank in [ Rank.Two, Rank.Three, Rank.Four, Rank.Five, Rank.Six, Rank.Seven, Rank.Eight, Rank.Nine, Rank.Ten, Rank.Jack, Rank.Queen, Rank.King, Rank.Ace ] :

				self.Deck.append( Card( suit, rank ) )		# create and append card object to self.Deck


		# Prepare a data structure to store player information:

		self.Player = []

		for ii in range( numPlayers ) :

			self.Player.append( { 'hand': [], 'bids': [], 'tricks': [], 'points': [] } )		# Give each player a dictionary containing empty lists which will store the following values:

			# hand: The current hand of the player, that is the cards he is holding while playing a round.

			# bids: List of 



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


	def _circDec( self, num ) :

		'''
		Decrements 'num' by 1 and rotates it round back to (self.numPlayers - 1) if the new number falls belows zero.

		Used internally to decrement the player number/ID.
		'''

		if num == 0 :

			return self.numPlayers

		else :

			return num - 1

	


	def Deal( self ) :

		'''
		This method implements the cards being dealt for a new round.
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

				self.Player[ player ][ 'hand' ].append( shuffled[ index ] )		# We keep track of the cards by referring to their index position in self.Deck and not the cards themselves

				index += 1


		# The next card from the deck will determine the trump:

		self.TrumpCard = self.Deck[ shuffled[ index ] ]

		
		# Store the trump based on the TrumpCard dealt:

		self.trump = self.TrumpCard.Suit

		self.trump.trump = True			# Tell the trump suit that it has been declared trump



	
	def Bid( self, player, bid ) :

		'''
		This method implements the interface for a player making a bid for a new round.

		The player who is meant to be bidding is tracked and an exception is thrown if the order goes wrong. The interface to the Blackout class is required to correctly call self.Bid(). If an incorrect bid is made the method will return False to indicate so.

		player: <INT> The ID of the player who is making the big.

		bid: <INT> The number of tricks the specified player is bidding this round.


		The method returns True is a correct bid value has been specified, it returns False otherwise. For other errors an exception is thrown.
		'''

		# We check that a legal player ID has been passed

		assert 0 <= player < self.numPlayers, 'ERROR: Illegal Played ID. It is required that 0 <= player <= numPlayers'


		# Check that a legal bid has been made

		if bid < 0 or bid > self.numTricks :			# Incorrect bid made

			return False

		
		# Now we check that the correct player is bidding, that is the bidding order is being maintained.

		assert player == self.Bidder, 'ERROR: Player is bidding out of turn. Current player that should be bidding is Player %d' % self.Bidder


		# Since all the checks have been cleared we place the bid:

		self.Player[ player ][ 'bid' ] = bid


		# Special care must be taken when the dealer is bidding:

		if self.Bidder == self.Dealer :

			# The total number of bids must not be equal to the total number of tricks

			totalBids = 0

			for ii in range( self.numPlayers ) :	totalBids += self.Player[ ii ][ 'bid' ]

			if totalBids == self.numTrics :			# The total number of bids is equal to the number of tricks in this round.

				return False
		

		# Increment the bidder:

		self.Bidder = self._circInc( self.Bidder )

		
		# We now check whether the bidding has gone beyond the full circle:

		assert self.Bidder != self.Leader, 'ERROR: Bidding has progressed beyond full circle. More bids than players.'


		# Correct bid made:

		return True




	def Move( self, player, card_index ) :

		'''
		This method implements an interface by which the class is informed about the next move.

		player: <INT> The ID of the player who is playing the card. This is checked against the internal state of the game for validity. An exception is thrown if it is invalid.

		card_index: <INT> The index in self.Player[ player ][ 'hand' ] (list) which points to the card the player has chosen to play from his hand on this move.
		

		This method will validate the card played by checking if the player has the card to begin with and if so whether the move is legal, that is, is he following suit if he can. Valid moves will return True, invalid ones will return False. It is the responsibility of the interfacer to check these boolean values before moving forward.
		'''

		assert player == self.Current, 'ERROR: Player making move out of turn.'

		assert self.Player[ player ][ 'hand' ] != [], 'ERROR: No cards left in the players hand'

		assert card_index >= 0 and card_index < len( self.Player[ player ][ 'hand' ] ), 'ERROR: Player has issued a card index that is out of bounds of the list describing the player\'s hand'



		card = self.Deck[ self.Player[ player ][ 'hand' ][ card_index ] ]

		
		# Now we check the validity of the move:

		if player == self.Leader :		# The player is the leader and so can play any card from his hand

			# We first check for overflow of tricks play where the tricks played have circled round and the leader is playing a card again

			assert self.currentTrick[ self.Leader ] == None, 'ERROR: The leader has submitted two cards to a single trick.'


			card.Suit.led = True		# Declare the suit played by the leader to be the suit that has been led in this trick

			self.ledSuit = card.Suit	# The Object is told what suit has been led


		else :			# The player is NOT the leader and we have to check the validity of the move

			if not card.Suit is self.ledSuit :		# Not following suit:

				# We now check if the player has a card in his hand of the suit led in which case this current move is invalid

				for item in self.Player[ player ][ 'hand' ] :

					if item.suit is self.ledSuit :			# Invalid move the player had the suit led

						return False
		
		# If execution gets here the move was valid. We prepare for the next move:

		self.Current = self._circInc( self.Current )


		# We add the played card to the sequence of cards played and remove it from the players hand all at the same time using the list's pop feature:

		self.currentTrick[ player ] = self.Player[ player ][ 'hand' ].pop( card_index )		# We store which card was played by which player


		return True		# Valid move




	def evalTrick( self ) :

		'''
		This method first verifies that every player has played a card in the current trick and then evaluates the trick to determine the winner of the trick. It then performs certain house-keeping duties to make way for the next trick.
		'''













			


	

	def postRound( self ) :

		'''
		This method is intended to be called after each round is played. It is used to clear and prepare anew the various variables that are used within each round. It prepares these variables/members for the next round.
		'''
		
		# Clear the trump and led suit indicators

		self.trump.trump = False
		self.led.led = False

		# Clear the player hands

		for ii in range( self.numPlayers ) :

			self.Player[ii][ 'hand' ] = []		# Clear the lists to indicate empty hands for each player


		# Advance the dealer, the leader and the bidder in preparation for the next round :

		self.Dealer = self._circInc( self.Dealer )
		self.Leader = self.Dealer
		self.Bidder = self.Leader


		# The following values set are done at the end of each trick and must be performed before every new round since the position of the leader changes

		self.currentTrick[ self.Leader ] = None		# Empty the trick played by the leader. We will use this to test for overflow of tricks played.
		self.currentTrick[ self.Dealer ] = None		# We use this to check whether all players have played cards in a given trick


		# Advance the round number:

		self.Round += 1
		

		# Advance the number of tricks

		if self.Round > self.maxTricks :		# The new Round number is greater than the max no. of tricks (globally) allowed and so we are in the decreasing trick phase of the game

			self.numTricks -= 1

		else :
			
			self.numTricks += 1


		# We check for end of game:

		assert self.numTricks != 0, 'ERROR: One too many calls to postRound() have been made. The game has already ended.'		# numTricks decremented to zero.

			







def circGen( total, start ) :

	'''
	This is a generator which creates a sequence of integers starting with the value 'start' which goes up to 'total - 1' and then circles back around to begin from zero. A single iteration is created.
	'''

	assert start > -1, 'ERROR: start must be a positive integer preferably between 0 and (total - 1)'


	start = start % total		# We allow for the fact that start might be outside of total already


	for ii in range(total) :

		yield (ii + start) % total
