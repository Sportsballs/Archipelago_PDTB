from .Bunnies import pinkBunnies, sunkenBunnies, hayBunnies, \
        spookyBunnies, forgottenUpperBunnies, forgottenMiddleBunnies, \
        forgottenLowerBunnies, templeBunnies, \
        falseHellBunnies, sleepHellBunnies, crumblingHellBunnies, \
        hellTempleBunnies, pillarsBunny, south20Bunny, \
        southTempleBunnies, forgotten9Bunnies, forgotten8Bunny, \
        Bunny

from BaseClasses import Location, CollectionState
from .Consts import PaqueretteGame


class PaqueretteLocation(Location):
    game: str = PaqueretteGame


# The truth is, all these "locations" are
# actually bnuuys that could be captured.


class PaqueretteBunLocation(PaqueretteLocation):
    game: str = PaqueretteGame

    def __init__(self, player: int, name: str, id: int, bun: Bunny, use_expert: bool, use_home_captures: bool):
        super().__init__(player, name, id)
        self.bun: Bunny = bun
        self.use_expert: bool = use_expert
        self.use_home_captures: bool = use_home_captures

    def access_rule(self, state: CollectionState):
        if not self.bun.requires:
            return True

        if any(requirement.satisfied(state, self.player)
               for requirement in self.bun.requires):
            return True

        if self.use_expert and any(requirement.satisfied(state, self.player)
                for requirement in self.bun.expert):
            return True

        if self.use_home_captures is False:
            return any(requirement.satisfied(state, self.player) for requirement in self.bun.expertNoHome)

        return False


def makeLocationName(mapName: str, index: int) -> str:
    return mapName + "-" + str(index)


def generateBunnyLocation(playerId, bunny: Bunny, expertRouting: bool, homeCaptures: bool) \
        -> PaqueretteBunLocation:
    name = makeLocationName(bunny.map, bunny.index)
    return PaqueretteBunLocation(playerId, name, location_name_to_id[name], bunny, expertRouting, homeCaptures)



def generateRegionBunnies(playerId,
                          regionBunnies: list[Bunny],
                          expertRouting: bool,
                          homeCaptures: bool) -> list[PaqueretteBunLocation]:
    return [
            generateBunnyLocation(playerId, bunny, expertRouting, homeCaptures)
            for bunny in regionBunnies
            ]


# locations dictionary generation


def getNextLocationID() -> int:
    global last_location_id
    last_location_id += 1
    return last_location_id


def generateLocationTupleFromBunny(bunny: Bunny) -> tuple[str, int]:
    return (makeLocationName(bunny.map, bunny.index), getNextLocationID())


def generateLocationTuples(*bunnyCollections: list[Bunny]) -> list[tuple[str, int]]:
    return [
            generateLocationTupleFromBunny(bunny)
            for bunnies in bunnyCollections
            for bunny in bunnies
            ]


last_location_id = 1

list_of_credits_bunnies = generateLocationTuples(pinkBunnies,
                                         sunkenBunnies,
                                         hayBunnies,
                                         spookyBunnies,
                                         forgottenUpperBunnies,
                                         forgottenMiddleBunnies,
                                         forgotten9Bunnies,
                                         forgottenLowerBunnies,
                                         templeBunnies,
                                         southTempleBunnies,
                                         forgotten8Bunny,
                                         falseHellBunnies)



list_of_bunnies = list_of_credits_bunnies + generateLocationTuples(
                                         sleepHellBunnies,
                                         crumblingHellBunnies,
                                         southTempleBunnies,
                                         south20Bunny,
                                         hellTempleBunnies,
                                         pillarsBunny)

list_of_locations = list_of_bunnies

location_name_to_id = {location[0]: location[1]
                       for location in list_of_locations}
location_id_to_name = {location[1]: location[0]
                       for location in list_of_locations}
