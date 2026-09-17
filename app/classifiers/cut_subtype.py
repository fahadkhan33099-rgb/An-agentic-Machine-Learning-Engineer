"""Optional MovieCuts mapping; no subtype is invented without model evidence."""
MOVIECUTS_TO_TAXONOMY = {"cross_cut":"Cross Cut", "cutaway":"Cutaway", "cutting_on_action":"Cutting on Action", "jump_cut":"Jump Cut", "match_cut":"Match Cut", "reaction_cut":"Reaction Cut", "smash_cut":"Smash Cut", "speaker_change":"Speaker Change", "standard_cut":"Standard Cut"}
def map_moviecuts_label(label: str | None) -> str | None: return MOVIECUTS_TO_TAXONOMY.get((label or "").lower())
