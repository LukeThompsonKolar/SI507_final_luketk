import unittest
import pokemon as poke
import json
import sqlite3

#1
class TestDB(unittest.TestCase):

    def testConstructor(self):
        conn = sqlite3.connect('pokemon.db')
        cur = conn.cursor()
        c = cur.execute("SELECT * FROM Pokemon").fetchall()
        c2 = cur.execute("SELECT * FROM Stats").fetchall()
        self.assertEqual(len(c),807)
        self.assertEqual(len(c2[0]),8)

class TestCondition(unittest.TestCase):

    def testVal(self):
        self.assertTrue(poke.Condition("attack>40").val)
        self.assertTrue(poke.Condition("attack=40").val)
        self.assertTrue(poke.Condition("attack<40").val)
        self.assertFalse(poke.Condition("attack>h").val)
        self.assertFalse(poke.Condition("atack>40").val)

class TestCheck(unittest.TestCase):

    def testCheckType(self):
        self.assertTrue(poke.check_type("water"))
        self.assertFalse(poke.check_type("wat"))

    def testTypeColors(self):
        self.assertEqual(poke.type_colors("Dark"),"rgb(0,0,0)")

class TestCommand(unittest.TestCase):

    def testBarCommand(self):
        c1 = poke.process_command("bar stat=total")
        c2 = poke.process_command("bar stat=specialattack cond:speed=150 bottom=5")
        self.assertEqual(len(c1[0]),5)
        self.assertEqual(c1[1],"bar")
        self.assertEqual(c1[2],"Total")
        self.assertEqual(c2[0][0][0],"Electric")

    def testScatterCommand(self):
        c1 = poke.process_command("scatter stat=total type=grass,fire")
        c2 = poke.process_command("scatter stat=specialattack type=all")
        self.assertEqual(c1[0][0][0],"Bulbasaur")
        self.assertEqual(len(c2[0]),807)
        self.assertEqual(c1[1],"scatter")
        self.assertEqual(c1[2][0],["Grass","Fire"])
        self.assertEqual(c2[2][1],"Specialattack")

    def testHistCommand(self):
        c1 = poke.process_command("hist height count")
        c2 = poke.process_command("hist type=poison weight density")
        self.assertEqual(c1[0][0][0],0.71)
        self.assertEqual(len(c2[0]),66)
        self.assertEqual(c2[0][2][0],100.0)
        self.assertEqual(c1[1],"hist")
        self.assertEqual(c1[2][0],None)
        self.assertEqual(c2[2][0],"Poison")
        self.assertTrue(c2[2][2])
        self.assertEqual(c1[2][2],"Heights")

    def testBoxCommand(self):
        c1 = poke.process_command("box stat=height")
        c2 = poke.process_command("box type=poison,fire stat=hp")
        self.assertEqual(c1[0][0][0],0.71)
        self.assertEqual(len(c2[0]),128)
        self.assertEqual(c2[0][3][0],39)
        self.assertEqual(c1[1],"box")
        self.assertEqual(c1[2][0],[])
        self.assertEqual(c2[2][0],["Poison","Fire"])
        self.assertEqual(c2[2][1],"Hp")

    def badCommand(self):
        self.assertEqual(poke.process_command("fghgfh")[0],None)
        self.assertEqual(poke.plot([],"bar"),None)

unittest.main()
