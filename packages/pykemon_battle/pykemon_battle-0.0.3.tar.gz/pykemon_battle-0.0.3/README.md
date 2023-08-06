[![Tests][tests-shield]][tests-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

A text-based Pokémon battling system
========================================


<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#tests">Tests</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



## About The Project
`pykemmon_battle` is a library that provides a text-based Pokémon battling system. 


## Installation
Quick installation instructions:

    $ python -m pip install pykemon_battle

Install a development version of this library by cloning the repository and running `flit`:
    
    $ git clone https://github.com/11michalis11/pykemon_battle.git
    $ cd pykemon_battle
    $ python -m pip install flit
    $ python -m flit install --symlink


## Usage
Include the following in a python script:

```python
import pykemon_battle as pkm

team_size = 3
new_battle = pkm.Battle(team_size)
new_battle.start_battle()
```
Then run the script in your terminal:

    $ python my_script.py


## Tests
Run all tests developed by first installing and then running `tox`:

    $ python -m pip install tox
    $ python -m tox


## Roadmap
See the [open issues](https://github.com/11michalis11/pykemon_battle/issues) for a list of proposed features (and known issues).


## License
Distributed under the MIT License. See `LICENSE` for more information.


## Contributing
1. Fork the repository
2. Clone the forked repository
3. Create a new branch
4. Apply changes to the `pykemon_battle` library
5. Run tests and make sure they pass
6. Commit changes
7. Push changes to GitHub
8. Open PR on GitHub


## Contact
Michalis Panayides - [@Michalis_Pan](https://twitter.com/Michalis_Pan) - PanayidesM@cardiff.ac.uk

Project Link: [pykemon_battle](https://github.com/11michalis11/pykemon_battle)



<!-- MARKDOWN LINKS & IMAGES -->
[tests-shield]: https://img.shields.io/badge/Tests-passing-GREEN.svg
[tests-url]: https://github.com/11michalis11/pykemon_battle/actions
[issues-shield]: https://img.shields.io/github/issues/11michalis11/pykemon_battle.svg
[issues-url]: https://github.com/11michalis11/pykemon_battle/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg
[license-url]: https://github.com/11michalis11/pykemon_battle/blob/master/LICENSE.txt
