# Author: Abid H. Mujtaba
# Date: Jan. 21, 2012

# This file implements the Blackout class which can be considered the Kernel of the Blackout web-application (being implemented using Django). The purpose of the class is to implement an entire game of Blackout in an abstract fashion which can then be interfaced using the designed class API to play the game either by a terminal or the internet via a web server.

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

	pass


class Suit:

	'''
	This is basically an implementation of an enum (enumerated) type to represent the four suits a card can have in a deck.

	This implementation is based on the solution given by Aaron Maenpaa (edited Nov 30, 2010) on http://stackoverflow.com/questions/36932/whats-the-best-way-to-implement-an-enum-in-python

	It allows one to restrict the enum elements, makes sure that they are NOT simply integers, while allowing comparisons to be made. The way it works is that we create this class which we use to construct the elements. We then store the elements as members of the class itself and that allows one to use it as an enumeration. More elements with the same name should NOT be added at run-time.

	One can now assign these to variables. For example:

	a = Suit.Spade	# means the variable contains a spade
	'''

	def __init__( self, name ) :

		self.name = name

		self.trump = False		# This declares that this suit is not trump (at least not yet). The way the enumerated type is being implemented, if this value is changed for any variable containing the enumerated type it will change simultaneously for all variables that contain that enumerated type (suit)

		self.led = False		# This declares that this suit was NOT led (at least not yet). This behaves like the trump member.

	def __str__( self ) :
			
		return "<Suit: %s>" % self.name

	def __repr__( self ) :

		return str( self )



# We use the Suit class to create the enumerated type elements explicitly:

Suit.Spade = Suit( 'Spade' )		
Suit.Heart = Suit( 'Heart' )
Suit.Club = Suit( 'Club' )
Suit.Diamond = Suit( 'Diamond' )

# We store a particular instance (object) of the class in the class (and not in an object) itself as a member. Now Suit.Spade is a particular Suit instance distinct from any other.
#
# Example:
# 
# a = Suit.Spade
# b = Suit.Spade
#
# bool( a == b )		# This returns True so comparisons can be made.
#
# a.trump		# Initially False
# Suit.Spade.trump = True		# Declare spades to be trump
# a.trump		# Now True
# b.trump		# Now True

# The same goes for Suit.Spade.led = True which declares that Spades were led in the current hand/round. The Blackout class must explicitly take care of the problem of more than one suit being declared trump or led simultaneously. Between hands/rounds care must be taken to set these values back to False again.

# Be careful. The code doesn't check if two suits have erroneously been declared trump.



class Rank:

	'''
	This implements an enum to represent the rank of a card that is the number associated with it: 2 - 10, J, Q, K, A

	It is based on the same logic as the Suit class
	'''

	def __init__( self, rank ) :

		'''
		This creates an instance of the class. The rank argument is an integer denoting the rank of the card with J:11, Q:12, K:13 and A:14.
		'''

		assert rank > 1, 'ERROR: Rank assigned is not in the range 2 to 14 inclusive as dictated by a Deck of Cards'
		assert rank < 15, 'ERROR: Rank assigned is not in the range 2 to 14 inclusive as dictated by a Deck of Cards'

		self.rank = rank 	 # This is an integer value which denotes the rank of the card.

		self.stringList = ['','', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A' ] 	# Stores string representations of the ranks
	


	def __gt__( self, other ) :

		'''
		We are overloading the greather than ( > ) operator so that it tells us if one rank is greather than the other.
		'''

		if self.rank > other.rank :

			return True
		
		else :

			return False

	
	
	def __str__( self ) :

		return "<Rank: %s>" % self.stringList[ self.rank ]		# Return the string representation of the rank of the suit 	


	def __repr__( self ) :

		return self 


# We use the Rank class to create the enumerated type elements explicitly, to correspond to the allowed ranks of cards:

Rank.Two = Rank(2)
Rank.Three = Rank(3)
Rank.Four = Rank(4)
Rank.Five = Rank(5)
Rank.Six = Rank(6)
Rank.Seven = Rank(7)
Rank.Eight = Rank(8)
Rank.Nine = Rank(9)
Rank.Ten = Rank(10)
Rank.Jack = Rank(11)
Rank.Queen = Rank(12)
Rank.King = Rank(13)
Rank.Ace = Rank(14)



class Card:

	'''
	This card implements a single card of a deck. It basically contains a suit and a rank signifying a card. For the sake of simplicity it is NOT being implemented as an enumerated type.
	'''

	def __init__( self, suit, rank ) :

		# simply store the passed values
		
		self.Suit = suit
		self.Rank = rank

	
	def __gt__( self, other ) :

		'''
		We overload the greater than operator allowing us to rank cards amongst each other. This function uses the suits' self-knowledge about them being trump and/or led or not.
		'''

		# We check that either we are dealing with the same suit or if they are different suits then they are NOT both trump and/or NOT both designated as the suit that was led in the current hand

		if not self.Suit == other.Suit :		# If the two Suits are not the same perform some checks

			assert not ( self.Suit.trump and other.Suit.trump ), 'ERROR: Two suits cannot be Trump at the same time.'
			assert not ( self.Suit.led and other.Suit.led ), 'ERROR: Two suits cannot have been led in the current hand at the same time.'


		if self.Suit == other.Suit :		# The two suits match we should compare ranks. Uses overloading of equality operator in class Suit.

			if self.Rank > other.Rank :		# Rank precedence established. User overloading of greather than operatore in class Rank.

				return True

			else :

				return False

		else :					# Suits did not match. Check for trump and which suit was led.

			if self.Suit.trump or other.Suit.trump :		# One of the two (distinct) suits is trump. (Both can't be because we checked via assertion).

				if self.Suit.trump :		# self is the Trump suit

					return True		# Trump suit beats non-trump suit regardless of rank

				else :
					return False

			elif self.Suit.led or other.Suit.led :			# Neither suit is trump but one or the other was the suit led in this hand which gives it precedence regardless or rank

				if self.Suit.led :		# self.Suit was the one led and so it has precedence

					return True

				else :

					return False			# Neither suit is trump so no rank precedence can be established

			else :		# Neither suit was trump or led in which case no precedence exists

				return False

		


	def __str__( self ) :

		return "<Card:  %s %s>" % ( self.Suit.name, self.Rank.stringList[ self.Rank.rank ] )


	def __repr__( self ) :

		return str(self)
