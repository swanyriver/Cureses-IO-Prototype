Testing curses library on flip server
Result: success!

To run the test:
python cursesIO.py 2>/dev/null

the redirect is necesary because I use the stderr channel to perform logging (by directing it to a pipe then running tail on that pipe) but if its not redirected it shares the stdout with curses and causes problems

I also tried out 3 different methods for looping between Input and Output and they can be tested by supplying the commandline arg {1-3}
python cursesIO.py 1 2>/dev/null  // input is consumed/processed immediately, and checking for input is non halting, screen refreshes on an interval
python cursesIO.py 2 2>/dev/null  // input is gathered and processed each time the screen is refreshed
python cursesIO.py 3 2>/dev/null  // halfbreak method is used, input is waited for but input times out after n-Tenths of a second (not viable)

