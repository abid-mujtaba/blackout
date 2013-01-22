# Author: Abid H. Mujtaba
# Date: Jan. 22, 2012

# This file implements Unit tests for the various classes and functions in the Blackout scripts

import unittest
from blackout import *		# import all classes and functions from blackout.py

class testBlackout( unittest.TestCase ) :

	'''
	Inherited class to unit test the Blackout functions and class.
	'''

	def test_circGen( self ) :

		'''
		Unit Test for the circGen function. 

		Definition: circGen( total, start)

		Functionality: circGen is a generator which will start with the value 'start' (or 'start % total' if start >= total) and will iterate up to (total - 1) and will then loop around to 0 and iterate up to start - 1. So it basically implements a circular range generator.
		'''

		# Basic functionality:

		self.assertEqual( list( circGen( 4, 2 ) ), [2, 3, 0, 1] )

		self.assertEqual( list( circGen( 8, 3 ) ), [3, 4, 5, 6, 7, 0, 1, 2] )


		# Edge cases:

		self.assertEqual( list( circGen( 4, 0 ) ), [0, 1, 2, 3] )

		self.assertEqual( list( circGen( 4, 3 ) ), [3, 0, 1, 2] )


		# Bleed over cases:

		self.assertEqual( list( circGen( 4, 4 ) ), [0, 1, 2, 3] )
		
		self.assertEqual( list( circGen( 4, 5 ) ), [1, 2, 3, 0] )


	
	def test_Suit( self ) :

		'''
		Unit Test for class Suit which implements a suit enumeration.
		'''

		s = Suit.Spade
		h = Suit.Heart
		c = Suit.Club
		d = Suit.Diamond

		# Verify strings

		self.assertEqual( str(s), '<Suit: Spade>' )
		self.assertEqual( str(h), '<Suit: Heart>' )
		self.assertEqual( str(c), '<Suit: Club>' )
		self.assertEqual( str(d), '<Suit: Diamond>' )


		# Verify trump = False initially:

		for item in [s, h, c, d] :

			self.assertEqual( item.trump, False )
			self.assertEqual( item.led, False )


		# Declare new variable with same suit:

		s2 = Suit.Spade

		self.assertEqual( s, s2 )

		# Change value of trump:

		Suit.Spade.trump = True

		
		# Verify that this change now effects all variables containing Suit.Spade

		self.assertEqual( s.trump, True )
		self.assertEqual( s2.trump, True ) 


		# Same for led:

		h2 = Suit.Heart

		Suit.Heart.led = True

		self.assertEqual( h.led, True )
		self.assertEqual( h2.led, True )

	

	def testRank( self ) :

		'''
		Unit Test for Rank class.
		'''
		
		r2 = Rank.Two
		r5 = Rank.Five
		r9 = Rank.Nine
		rQ = Rank.Queen
		rA = Rank.Ace


		r_9 = Rank.Nine
		r_A = Rank.Ace

		
		# Establish equality of enumerated type:

		self.assertEqual( r9, r_9 )
		self.assertEqual( rA, r_A )


		# Establish precedence:

		self.assertEqual( r2 > r2, False )
		
		self.assertEqual( r2 > r5, False )
		self.assertEqual( r5 > r2, True )

		self.assertEqual( r2 > rA, False )
		self.assertEqual( rA > r2, True )

		self.assertEqual( r9 > rQ, False )
		self.assertEqual( rQ > r9, True )
		self.assertEqual( rQ > rQ, False )


	
	def testCard( self ) :

		'''
		Unit Test for Card class.
		'''

		s3 = Card( Suit.Spade, Rank.Three )
		c3 = Card( Suit.Club, Rank.Three )
		cJ = Card( Suit.Club, Rank.Jack )
		sQ = Card( Suit.Spade, Rank.Queen )
		h7 = Card( Suit.Heart, Rank.Seven )
		d9 = Card( Suit.Diamond, Rank.Nine )


		# Establish precedence scheme. So far no suit is trump or has been led:

		self.assertEqual( s3 > s3, False )
		self.assertEqual( s3 > sQ, False )
		self.assertEqual( sQ > s3, True )

		self.assertEqual( s3 > c3, False )
		self.assertEqual( c3 > s3, False )

		self.assertEqual( c3 > h7, False )
		self.assertEqual( h7 > c3, False )


		# Declare club to trump:

		Suit.Club.trump = True

		self.assertEqual( sQ > c3, False )
		self.assertEqual( c3 > sQ, True )
		self.assertEqual( c3 > h7, True )
		self.assertEqual( c3 > d9, True )

		self.assertEqual( c3 > cJ, False )
		self.assertEqual( cJ > c3, True )


		# Declare space to have been led :

		Suit.Spade.led = True

		self.assertEqual( s3 > sQ, False )
		self.assertEqual( sQ > s3, True )

		self.assertEqual( s3 > h7, True )
		self.assertEqual( s3 > d9, True )

		self.assertEqual( s3 > c3, False )
		self.assertEqual( c3 > sQ, True )


		# Clear trump and led for later tests:

		Suit.Club.trump = False
		Suit.Spade.led = False 










if __name__ == '__main__' :

	unittest.main()
