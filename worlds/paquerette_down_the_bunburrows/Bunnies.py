# Bnuuy are locations
# locations also are beholden to their region restrictions
from BaseClasses import CollectionState


class AccessRequirement():
    def __init__(self):
        self.tools: list[str] = list()
        self.regions: list[str] = list()

    def satisfied(self, state: CollectionState, player):
        regionAccess = (not self.regions or all(
                    state.can_reach(region, "Region", player)
                    for region in self.regions))

        if not self.tools:
            return regionAccess

        return (all(state.has(tool, player, 1) for tool in self.tools)
                and regionAccess)


class Bunny():
    def __init__(self, map: str, index: int):
        self.map = map
        self.index = index
        self.requires: list[AccessRequirement] = list()
        self.expert: list[AccessRequirement] = list()
        self.expertNoHome: list[AccessRequirement] = list()

    def Needs(self, *ids: str, regions=None):
        if regions is None:
            regions = []

        req = AccessRequirement()
        req.tools = list(ids)
        req.regions = regions

        self.requires.append(req)
        return self

    def Expert(self, *ids: str, regions=None):
        if regions is None:
            regions = []

        req = AccessRequirement()
        req.tools = list(ids)
        req.regions = regions

        self.expert.append(req)
        return self

    def NoHome(self, *ids: str, regions=None):
        if regions is None:
            regions = []

        req = AccessRequirement()
        req.tools = list(ids)
        req.regions = regions

        self.expertNoHome.append(req)
        return self


def Bun(map: str, index: int = 1) -> Bunny:
    bun = Bunny(map, index)
    return bun


pinkBunnies = [
        Bun("W-1"),
        Bun("W-2"),
        Bun("W-3"),
        Bun("W-4"),
        Bun("W-5"),
        Bun("W-6", 1),
        Bun("W-6", 2),
        Bun("W-7").Needs("C-7", regions=["Hay"]),
        Bun("W-8"),
        Bun("W-9"),
        Bun("W-10"),
        Bun("W-11"),
        Bun("W-12"),
        ]

sunkenBunnies = [
        Bun("N-1"),
        Bun("N-2").Needs("N-2"), 
        Bun("N-3").Needs("N-3").Expert(regions=["Hay"]), # Expert via C-3 (tools guaranteed)
        Bun("N-4").Needs("N-4").Expert("C-4", regions=["Hay"]), # Expert via C-4
        Bun("N-5").Needs("N-5"),
        Bun("N-6").Needs("N-6"),
        Bun("N-7").Needs("N-7").NoHome("C-7", regions=["Hay"]), # Non-Home Expert via C-7
        Bun("N-8").Needs("N-8").Expert("C-8", regions=["Hay"]), # Expert via C-8 by stacking with W-8
        Bun("N-9").Needs("N-9"),
        Bun("N-10").Needs("N-10").Expert("C-10", regions=["Hay"]), # Expert via C-10
        Bun("N-11").Needs("N-11")
        ]

hayBunnies = [
        Bun("C-1").Needs("C-1"),
        Bun("C-2").Needs("C-2"),
        Bun("C-3"),  # Tutorial level, tools guaranteed
        Bun("C-4").Needs("C-4"),
        Bun("C-5").Needs("C-5"),
        Bun("C-6").Needs("C-6"),
        Bun("C-7").Needs("C-7"),
        Bun("C-8").Needs("C-8"),
        Bun("C-9").Needs("C-9"),
        Bun("C-10").Needs("C-10"),
        Bun("C-11").Needs("C-11"),
        Bun("C-12").Needs("C-12")
        ]

spookyBunnies = [
        Bun("S-1").Needs("S-1"),
        Bun("S-2").Needs("S-2"),
        Bun("S-3").Needs("S-3"),
        Bun("S-4").Needs("S-4").NoHome("C-4"), # Non-Home Expert via C-4
        Bun("S-5"),  # No Tools
        Bun("S-6"),  # Tutorial level, tools guaranteed
        Bun("S-7").Needs("S-7"),
        Bun("S-8").Needs("S-8"),
        Bun("S-9").Needs("S-9"),
        Bun("S-10").Needs("S-10").NoHome("C-10"), # Non-Home Expert via C-10
        Bun("S-11").Needs("S-11"),
        Bun("S-12").Needs("S-12"),
        ]

# Rooms that require entry-level access (45 bunnies) to fully capture
forgottenUpperBunnies = [
        Bun("E-1").Needs("E-1"),
        Bun("E-2").Needs("E-2"),
        Bun("E-3", 1).Needs("E-3", "E-2").Expert(),  # Expert via C-3
        Bun("E-3", 3).Needs("E-3", "E-2").Expert(),  # Expert via C-3
        Bun("E-3", 2).Needs("E-3", "E-2"),
        Bun("E-3", 4).Needs("E-3", "E-2"),
        Bun("E-4").Needs("E-4", "E-3", "E-2").Expert("E-4", "E-3") # Expert via C-3 by edge digging in E-3
        ]
# BUG: The E-3-1, E-3-3, and E-4 expert captures are only in logic if you have 45 bunnies
# This will likely require creating a new region for these 3 bunnies in order to correctly define the logic
# As far as I'm aware, splitting the bunnies in E-3 into two seperate regions shouldn't cause issues
# I will try to have this fixed before submitting this big logic overhaul release - Sports

# Rooms require only E-5 and E-3 OR E-5 and C-5
# Not considered dependent upon Upper locations due to C-3
forgottenMiddleBunnies = [
        Bun("E-6").Needs("E-6"),
        Bun("E-7").Needs("E-6", "E-7")
        ]

# Want to be able to exclude E-8 from Credits-only runs
# Dependencies defined in region creation
forgotten8Bunny = [
        Bun("E-8")
        ]

# Hate making a separate record for this, but cant define rule correctly as is
# Accessible from above, OR from C-10 & E-10
forgotten9Bunnies = [
        Bun("E-9", 1).Needs("E-9"),
        Bun("E-9", 2).Needs("E-9"),
        ]

# Rooms require either Middle & 9 full access or C-10 access
forgottenLowerBunnies = [
        Bun("E-10", 1).Needs("E-10"),
        Bun("E-10", 2).Needs("E-10"),
        Bun("E-12", 1).Needs("E-10", "E-11"),
        Bun("E-12", 2).Needs("E-10", "E-11"),
        ]

templeBunnies = [
        Bun("C-13").Needs("S-13").NoHome(), # Non-Home Expert with only C-13 (which is a requirement for the region)
# BUG: It can be reasonably argued that the C-13 Non-Home capture shouldn't need expert routing to be in logic
# Currently as it stands, non-home captures are only in logic if expert routing is enabled
# Making a system which checks for non-expert, non-home captures would require another rework of access_rule function in Locations.py
# This is the only bunny that this would apply to (as far as I can tell), and non-expert, non-home is very likely a rarely meaningful option setting
# I probably won't be spending time to fix this right now - Sports

        Bun("W-13"),
        Bun("W-14").Needs("W-14"),
        Bun("W-15").Needs("W-15"),
        Bun("W-16").Needs("W-16"),
        Bun("W-17").Needs("W-17"),
        Bun("W-18").Needs("W-18"),

        Bun("N-12").Needs("N-12"),
        Bun("N-13", 1).Needs("N-13"),
        Bun("N-13", 2),
        Bun("N-13", 3),
        Bun("N-14").Needs("N-14"),
        Bun("N-15").Needs("N-15"),
        Bun("N-16").Needs("N-16"),
        Bun("N-17").Needs("N-17").NoHome("C-17"), # Non-Home Expert via C-17
        Bun("N-18").Needs("N-18")
        ]

# Region depends on either C-13 OR C-20
southTempleBunnies = [
        Bun("S-13").Needs("S-13"),
        Bun("S-14").Needs("S-14"),
        Bun("S-15").Needs("S-15"),
        Bun("S-16").Needs("S-16"),
        Bun("S-17").Needs("S-17"),
        Bun("S-18").Needs("S-18"),
        Bun("S-19").Needs("S-19"),
        ]

# Region depends on C-13 access and tools
falseHellBunnies = [
        Bun("C-14").Needs("C-14"),
        Bun("C-15").Needs("C-15"),
        Bun("C-16").Needs("C-16"),
        Bun("C-17").Needs("C-17"),
        Bun("C-18").Needs("C-18"),
        Bun("C-19").Needs("C-19"),
        ]

# Region already depends on E-13 access
sleepHellBunnies = [
        Bun("E-14"),
        Bun("E-15"),
        Bun("E-16").Needs("E-16"),
        Bun("E-17").Needs("E-17"),
        Bun("E-18").Needs("E-18"),
        Bun("E-19").Needs("E-19"),
        Bun("E-20").Needs("E-20"),
        Bun("E-21").Needs("E-20", "E-21").NoHome("E-20", "C-20"), # Non-Home Expert by stacking with E-20 and C-20
        Bun("E-22").Needs("E-20", "E-22").NoHome("E-20"), # Non-Home Expert by stacking with E-20
        ]

# Region depends on Sleep Hell, E-20 tools, and C-20 tools
crumblingHellBunnies = [
        Bun("C-20").Needs("C-20").NoHome("E-20"), # Non-Home Expert by stacking with E-20
# BUG: The C-20 capture assumes that C-20 tools are required due to the region it is placed in
# However, a Non-Home expert capture is possible without C-20 tools, which currently will not show in logic
# This can be easily resolved by moving this bunny to the sleepHell region above
# This should be a quick fix, I'll get it done before the big logic overhaul release - Sports

        Bun("C-21"), 
        Bun("C-22").Needs("C-22", "S-22").Needs("C-22", "E-22").NoHome("C-22"), # Non-Home Expert via either S-22 or N-22. Either S-22 or E-22 required for non-expert
        Bun("C-23").Needs("C-22"),
        Bun("C-24").Needs("C-22", "C-24"),

        Bun("W-19").Needs("W-19"),
        Bun("W-20").Needs("W-20"),

        Bun("W-21").Needs("W-21", "C-21").Expert("W-21").NoHome(), # Expert by edge digging in C-20, Non-Home Expert via C-21 by edge digging in C-20

        Bun("N-19", 1).Needs("N-19"),
        Bun("N-19", 2).Needs("N-19"),
        Bun("N-20", 1),
        Bun("N-20", 2),
        Bun("N-20", 3),
        Bun("N-20", 4),
        Bun("N-21").Needs("N-21"),
        Bun("N-22", 1).Needs("C-22"),
        Bun("N-22", 2).Needs("C-22"),
        Bun("N-23", 1).Needs("N-23", "C-22"),

        Bun("S-21", 1).Needs("S-21", "C-21").Expert("S-21").NoHome(), # Expert by edge digging in C-20, Non-Home Expert via C-21 by edge digging in C-20
        Bun("S-21", 2).Needs("S-21", "C-21").Expert("S-21").NoHome(), # Expert by edge digging in C-20, Non-Home Expert via C-21 by edge digging in C-20

        Bun("S-22").Needs("S-22", "C-22").Expert("S-22", "S-21").NoHome("S-21"), # Expert and Non-Home Expert by edge digging in both C-20 and S-21
        Bun("S-23").Needs("S-23", "C-22").Expert("S-23", "S-21"), # Expert by edge digging in both C-20 and S-21
        Bun("S-24", 1).Needs("S-24", "S-23", "C-22").Expert("S-24", "S-23", "S-21"), # Expert by edge digging in both C-20 and S-21
        Bun("S-24", 2).Needs("S-24", "S-23", "C-22").Expert("S-24", "S-23", "S-21"), # Expert by edge digging in both C-20 and S-21
        ]

# Separate region for generation purposes
south20Bunny = [Bun("S-20").Needs("S-20").NoHome("C-20")] # Non-Home Expert via C-20

hellTempleBunnies = [
        Bun("W-23").Needs("W-23"),
        Bun("W-24").Needs("W-24"),
        Bun("W-25").Needs("W-25"),
        Bun("W-26", 1).Needs("W-26"),
        Bun("W-26", 2).Needs("W-26"),
        Bun("C-26").Needs("W-26"),
        ]

pillarsBunny = [
        Bun("C-27")
]
