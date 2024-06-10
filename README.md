# Strawberry fields
Song retrieval using hummed query

## Usage
After cloning the repository, navigate into the project directory and install the required packages using pip with the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

To run the application:

```bash
python -m flask run
```
## Music Catalog Database
| Title | Album | Singer | Composer | Lyricist |
| ----- | ----- | ------ | -------- | -------- |
| Neelathamare | Neelathamara | Karthik | Vidyasagar | Vayalar Sarathchandra Varma |
| Ee Solomanum Shoshannayum | Amen | Preeti Pillai, Sreekumar Vakkiyil | Prashant Pillai | P.S.Rafeeque |
| Premikkumbol | Salt N' Pepper | P.Jayachandran, Neha Nair | Bijibal | Rafeeq Ahammed |
| Ethu Kari Raavilum | Bangalore Days | Haricharan | Gopi Sundar | Rafeeq Ahammed |
| Chellathamare | Hallo | K. S. Chithra | Alex Paul | Vayalar Sarath Chandra Varma |
| Vaathilil Aa Vaathilil | Ustad Hotel | Haricharan | Gopi Sundar | Rafeeq Ahammed |
| Ente Khalbile | Classmates | Vineeth Sreenivasan | Alex Paul | Vayalar Sarath Chandra Varma |
| Pehli Nazar Mein | Race | Atif Aslam | Pritam Chakraborty | Sameer Anjaan |
| Thumbi Vaa | Olangal | S. Janaki | Ilaiyaraaja | O. N. V. Kurup |
| Uyiril Thodum | Kumbalangi Nights | Sooraj Santhosh, Anne Amie | Sushin Shyam | Anwar Ali |
| Etho Sayahna | 10:30 am Local Call | Sachin Warrier | Gopi Sundar | Rafeeq Ahammed |
| Ethrayo Janmamai | Summer in Bethlehem | Srinivas, Sujatha | Vidyasagar | Gireesh Puthenchery |
| Madabhara Mizhiyoram | Malaikottai Vaaliban | Preeti Pillai | Prashant Pillai | P.S. Rafeeque |
| Vennila Chandana Kinnam | Azhakiya Ravanan | K. J. Yesudas, Shabnam | Vidyasagar | Kaithapram Damodaran Namboothiri |
| Ankhon Mein Teri | Om Shanti Om | Krishnakumar Kunnath (KK) | Vishal Dadlani, Shekhar Ravjiani | Vishal Dadlani |
| Partha Muthal Naale | Vettaiyaadu Vilaiyaadu | Bombay Jayashri, Unni Menon | Harris Jayaraj | Thamarai |
| Unakkul Naane | Pachaikili Muthucharam | Bombay Jayashri | Harris Jayaraj | Rohini |
| Kaise Mujhe | Ghajini | Benny Dayal, Shreya Ghoshal | A. R. Rahman | Prasoon Joshi |
| Guzarish | Ghajini | Javed Ali, Sonu Nigam | A. R. Rahman | Prasoon Joshi |
| Can You Hear The Music | Oppenheimer | N/A | Ludwig GÃ¶ransson | N/A |
| Despacito | Vida | Luis Fonsi, Daddy Yankee | Luis Fonsi, Erika Ender | Luis Fonsi, Erika Ender |
| Hey Jude | Hey Jude | Paul McCartney | Paul McCartney | Paul McCartney |
| Skyfall | Skyfall | Adele | Adele, Paul Epworth | Adele, Paul Epworth |
| Somebody That I Used to Know | Making Mirrors | Gotye, Kimbra | Gotye | Gotye |
| Aga Naga | Ponniyin Selvan: II | Shakthisree Gopalan | A. R. Rahman | Ilango Krishnan |
| L'amour est bleu | L'amour est bleu | Vicky Leandros | AndrÃ© Popp | Pierre Cour |
| Norwegian Wood (This Bird Has Flown) | Rubber Soul | John Lennon | John Lennon | John Lennon |
| Katchi Sera | Katchi Sera | Sai Abhyankkar | Sai Abhyankkar | Adesh Krishna |
| Aayiram kannumaay | Nokkethadhoorathu Kannum Nattu | K. S. Chithra | Jerry Amaldev | Bichu Thirumala |
| Summer Wine | Nancy in London | Nancy Sinatra, Lee Hazlewood | Lee Hazlewood, Suzi Jane Hokom | Lee Hazlewood, Suzi Jane Hokom |
| Can't Help Falling in Love | Blue Hawaii | Elvis Presley | Hugo Peretti, Luigi Creatore, George David Weiss | Hugo Peretti, Luigi Creatore, George David Weiss |
| Aaro Nee Aaro | Urumi | Shweta Mohan, K. J. Yesudas | Deepak Dev, Loreena McKennitt | Kaithapram Damodaran Namboothiri |
| Thuli Thuli Mazhaiyaai | Paiyaa | Haricharan, Tanvi Shah | Yuvan Shankar Raja | Na. Muthukumar |
| Attention | Voicenotes | Charlie Puth | Charlie Puth | Charlie Puth, Jacob Kasher Hindlin |
| Tharaka Pennale | N/A | Remya Vinayakumar, Syam Prasad | Madhu Mundakath | Sathyan Komalloor |
| Barbie Girl | Aquarium | Lene NystrÃ¸m, RenÃ© Dif | Aqua (Band) | Aqua (Band) |
| Bella ciao | N/A | N/A | N/A | N/A |
| Stairway to Heaven | Led Zeppelin IV | Robert Plant | Robert Plant, Jimmy Page | Robert Plant, Jimmy Page |
| Main Theme | The Good, The Bad and The Ugly | N/A | Ennio Morricone | N/A |
| Israyelin Nadhanaay | Jesus | K. G. Markose | Peter Cheranalloor | Baby John Kalayanthani |
| Shalom Aleichem | N/A | N/A | Kabbalists of safed | Kabbalists of safed |
| Omal Kanmani | Naran | Vineeth Sreenivasan, K. S. Chithra | Deepak Dev | Kaithapram Damodaran Namboothiri |
| Rasputin | Nightflight to Venus | Boney M. (R&B group) | Frank Farian, George Reyam, Fred Jay (Based on ÃœskÃ¼darâ€™a Gider Ä°ken) | Frank Farian, George Reyam, Fred Jay |     
| All My Loving | With the Beatles | Paul McCartney | Paul McCartney | Paul McCartney |
| Gulabi Ankhen | The Train | Mohammed Rafi | R. D. Burman | Anand Bakshi |
| Show Me the Meaning of Being Lonely | Millennium | Backstreet Boys (Vocal group) | Max Martin, Herbie Crichlow | Max Martin, Herbie Crichlow |
| Nel blu, dipinto di blu | La strada dei successi | Domenico Modugno | Domenico Modugno | Domenico Modugno, Franco Migliacci |
| Tu jÃ©sty fÃ¡tÄƒ | Foku DrÃ¡kuluj | Kanizsa Csillagai (Musical group) | ZoltÃ¡n HorvÃ¡th | ZoltÃ¡n HorvÃ¡th |
| Michelle | Rubber Soul | Paul McCartney | Paul McCartney | Paul McCartney |
| Andro Verdan | N/A | N/A | Slovenian Roma (Ethnic group) | Slovenian Roma (Ethnic group) |

### References

- Joan Serrà, Josep Ll. Arcos, *An Empirical Evaluation of Similarity Measures for Time Series Classification*, Jan 2014.
- Hiroaki Sakoe, Seibi Chiba, *Dynamic programming algorithm optimization for spoken word recognition*, February 1978.
- Ivan Fernandez Cocano, *Expanding the evaluation of Audio to Score Matching applying Audio Querying strategies*, August 2023.
- Colin Raffel, Daniel P. W. Ellis, *Large-Scale Contend-Based Matching of Midi and Audio Files*, January 2015.
- Matija Marolt, *A mid level melody based representation for calculating audio similarity*, January 2006.
- Matthias Mauch and Simon Dixon, *PYIN: A Fundamental Frequency Estimator Using Probabilistic Threshold Distributions*, May 2014.
- Neal Gallagher, *Savitzky-Golay Smoothing and Differentiation Filter*, January 2020.
- Pedro Cano, Eloi Batlle, *A Review of Audio Fingerprinting*, November 2005.
- Pavel Senin, *Dynamic Time Warping Algorithm Review*, January 2009.
- Tomasz Górecki, Maciej Łuczak, *The influence of the Sakoe–Chiba band size on time series classification*, January 2019.
- Ulrich Oberst, *The Fast Fourier Transform*, January 2007.
- Prajoy Podder, Tanvir Zaman Khan, Mamdudul Haque Khan, M. Muktadir Rahman, *Comparative Performance Analysis of Hamming, Hanning and Blackman Window*, June 2014.
- Lawrence Rabiner, Jont B. Allen, *Short-Time Fourier Analysis Techniques for FIR System Identification and Power Spectrum Estimation*, July 1977.
- Robert C. Maher, James W. Beauchamp, *Fundamental frequency estimation of musical signals using a two-way mismatch procedure*, April 1994.
