# pokergames-cli

A simple CLI application that will allow you to see what games are running across most US and some overseas poker rooms. This application communicates with the Poker Buddy game API. You can check out the Poker Buddy app here:

iOS: https://apps.apple.com/us/app/poker-buddy-live-poker/id1507289868?ls=1

Android: https://play.google.com/store/apps/details?id=com.pokernotify.poker_buddy

_Note: this entire project was just an exercise to practice my python chops, it isn't perfect_

### Prerequisites

```
pip3 install -r requirements.txt
```

### How to use

```
python3 main.py {name of venue}
```

### Example

```
python3 main.py hollywood stl poker
```
### What to expect
```
Hollywood STL Poker: 314-770-7600

150-0 $150 Mini Mega:
  tables:5
  waitlist:0
1-2 NL HOLDEM:
  tables:4
  waitlist:3
2-3 NL HOLDEM:
  tables:0
  waitlist:1
2-5 NL HOLDEM:
  tables:0
  waitlist:1
```
