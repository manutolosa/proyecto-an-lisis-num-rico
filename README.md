# Audio stenography
## User Manual
When running, the program asks if you want to perform a steganography process, extract a text, or do MSE and PSNR tests.
Associated text can be found [here.](https://www.overleaf.com/read/wyghzytcyjhd)
The algorithm works by doing an LSB but instead of making the changes on the least significant bit, they happen on an outer order.

When run, the program asks if the user wishes to specify a file that contains the order of bit modification o if they to use default hardcoded option.

Such a file (order.txt) would look like this.
```
0
00
0
0
0
0
0
0
0
0
1
3
2
2
3
1
2
3
2
0
0
0
00
0
4
```

Once the order has been defined, the user is prompted to choose among the following options: to encode a text message, to decode a message from a wav file, and to produce MSE and PSNR metrics from specified wav files.
### Known Issues
For encoding the program uses the character 'ÿ' for control, and as such, using it inside a message would result in truncating the message. The program would fail if a large enough message is used as input. In practice this can be ignored since a normal cuantity of text is used, but a generic implementation that would allow for any bit based form would be bound by LSB capacity limitations. However, this algorithm also allows for more than one message to be applied, however the user would have to ensure that no colission between orders would occur.
