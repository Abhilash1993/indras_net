from indra.entry_point import entry_point
import models.fashion
import models.forestfire
import models.sand
import models.wolfsheep

models = {
             1: ("Adam Smith's Fashion Model", models.fashion.main),
             2: ("Forest Fire", models.forestfire.main),
             3: ("Abelian Sandpile", models.sandpile.main),
             4: ("Schelling's Segregation Model", models.segregation.main),
         }


def main(args=None):
    entry_point(args, models)


if __name__ == "__main__":
    main()
