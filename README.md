# Enigma 0.1.1

## _My take on a python WWII enigma machine_

## author warning

while user input is an option, it is HIGHLY recommended that you
use the included config.csv file for your inputs as it gives the most
consistant results

## additional warnings

Please note that there are a LOT of edge cases that are not
handeld gracefully, so please be careful with your input
try not to have unnessissary spaces if you can

# to do

configurations of the starting positions of the roters
sanitizing user input from both the CLI and config.csv inputs

## guidelines for the message

remove ALL non-letters from the message (spaces are fine)
that includes any and all puncuation, emojis, and ritual imgs

# useage

how to use the code

# config.csv

by far the easyest way to use the program as you dont have user error of inputing either the rotors in the wrong order or missing/adding uninteded plugboard connections

## for lines 1 - 3

these lines MUST be CAPITALIZED
if you don't, program wont work

## for lines 4+

this lines MUST be LOWERCASE
as this denotes the start of the plugboard connections

## line 1

### rotor configuration

separated by commas
takes exactly 3 rotors in the flavor of roman numerals I - VIII
_ex. I,II,III_
you can throw them in any order you want
\_ex. V,III,VI or even VIII,VII,VI

## line 2

### relector configuration

this option can only be set to "B" or "C"
as those skews were the ones used in WWII

## line 3

### the message

_the important part
what you want to hide from the world
or just your boss_

this can have caps and spaces but no non-letter characters

## lines 4+

### Plugboard configurations

the plugboard is defined by two connected non-same letters
you cannot connect letters that have already been connected
there is a limit of 10 conncurent connections
it will throw an error and escape in a terrible format

example in config.csv
