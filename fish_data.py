"""
Fish species information database for the Aquarium Fish Classifier.
Contains detailed information about each of the 6 classified fish species.
"""

FISH_DATABASE = {
    "Bete": {
        "scientific_name": "Betta splendens",
        "common_names": "Siamese Fighting Fish, Betta",
        "family": "Osphronemidae",
        "origin": "Southeast Asia (Thailand, Cambodia, Vietnam)",
        "habitat": "Freshwater — shallow ponds, rice paddies, slow streams",
        "max_size": "6–8 cm (2.5–3 inches)",
        "lifespan": "2–5 years",
        "diet": "Carnivorous — insects, larvae, small crustaceans",
        "temperature": "24–30°C (75–86°F)",
        "ph_range": "6.0–8.0",
        "difficulty": "Easy",
        "description": "Betta fish are famous for their vibrant colors and flowing fins. Males are territorial and aggressive toward other males. They possess a labyrinth organ allowing them to breathe atmospheric air, enabling survival in low-oxygen waters. They are one of the most popular aquarium fish worldwide.",
        "emoji": "🐟",
        "color": "#ef4444"
    },
    "Cray": {
        "scientific_name": "Procambarus spp.",
        "common_names": "Crayfish, Crawfish, Crawdad, Freshwater Lobster",
        "family": "Cambaridae / Parastacidae",
        "origin": "Worldwide — North America, Europe, Australia",
        "habitat": "Freshwater — rivers, streams, ponds, swamps",
        "max_size": "10–20 cm (4–8 inches)",
        "lifespan": "2–5 years",
        "diet": "Omnivorous — plants, insects, small fish, detritus",
        "temperature": "18–24°C (65–75°F)",
        "ph_range": "6.5–8.0",
        "difficulty": "Easy to Moderate",
        "description": "Crayfish resemble small lobsters and are fascinating freshwater crustaceans popular in aquariums. They are bottom dwellers that love to dig, hide, and explore. Crayfish are hardy creatures that can adapt to various water conditions. They molt their exoskeleton as they grow and can regenerate lost limbs.",
        "emoji": "🦞",
        "color": "#f59e0b"
    },
    "Discuss": {
        "scientific_name": "Symphysodon spp.",
        "common_names": "Discus, King of the Aquarium, Pompadour Fish",
        "family": "Cichlidae",
        "origin": "South America (Amazon River basin)",
        "habitat": "Freshwater — slow-moving rivers, floodplain lakes",
        "max_size": "15–20 cm (6–8 inches)",
        "lifespan": "10–15 years",
        "diet": "Omnivorous — small invertebrates, algae, plant matter",
        "temperature": "26–30°C (82–86°F)",
        "ph_range": "5.0–7.0",
        "difficulty": "Advanced",
        "description": "Discus fish are often called the 'King of the Aquarium' due to their stunning disc-shaped bodies and brilliant color patterns. They are social fish that prefer to live in groups and require pristine water conditions. Their graceful swimming and vibrant hues make them one of the most prized aquarium species.",
        "emoji": "👑",
        "color": "#8b5cf6"
    },
    "Gold": {
        "scientific_name": "Carassius auratus",
        "common_names": "Goldfish, Common Goldfish, Fancy Goldfish",
        "family": "Cyprinidae",
        "origin": "East Asia (China)",
        "habitat": "Freshwater — ponds, lakes, slow rivers",
        "max_size": "15–30 cm (6–12 inches)",
        "lifespan": "10–25 years",
        "diet": "Omnivorous — flakes, pellets, vegetables, insects",
        "temperature": "18–24°C (65–75°F)",
        "ph_range": "6.5–8.0",
        "difficulty": "Easy",
        "description": "Goldfish are one of the earliest domesticated fish and the most popular aquarium species worldwide. Originally bred in China over 1,000 years ago, they come in hundreds of varieties with diverse body shapes, fin types, and colors. Despite their reputation, goldfish can live for decades with proper care.",
        "emoji": "🐠",
        "color": "#f97316"
    },
    "Guppy": {
        "scientific_name": "Poecilia reticulata",
        "common_names": "Guppy, Millionfish, Rainbow Fish",
        "family": "Poeciliidae",
        "origin": "South America (Venezuela, Trinidad, Barbados)",
        "habitat": "Freshwater — streams, ponds, canals",
        "max_size": "3–6 cm (1.2–2.4 inches)",
        "lifespan": "1–3 years",
        "diet": "Omnivorous — algae, small insects, flakes, brine shrimp",
        "temperature": "22–28°C (72–82°F)",
        "ph_range": "6.8–7.8",
        "difficulty": "Easy (Beginner-friendly)",
        "description": "Guppies are small, colorful livebearers that are among the most popular aquarium fish for beginners. Males display dazzling tail patterns and colors to attract females. They are prolific breeders, earning the nickname 'Millionfish.' Guppies are peaceful, hardy, and thrive in community tanks.",
        "emoji": "🌈",
        "color": "#06b6d4"
    },
    "Oscar": {
        "scientific_name": "Astronotus ocellatus",
        "common_names": "Oscar, Tiger Oscar, Marble Cichlid, Velvet Cichlid",
        "family": "Cichlidae",
        "origin": "South America (Amazon, Orinoco, Paraguay river basins)",
        "habitat": "Freshwater — slow-moving rivers, canals, ponds",
        "max_size": "25–40 cm (10–16 inches)",
        "lifespan": "10–20 years",
        "diet": "Omnivorous — insects, fish, crustaceans, pellets",
        "temperature": "23–28°C (73–82°F)",
        "ph_range": "6.0–8.0",
        "difficulty": "Moderate",
        "description": "Oscar fish are large, intelligent cichlids known for their personality and ability to recognize their owners. They have expressive eyes and can learn to beg for food. Oscars are often considered 'water puppies' due to their interactive behavior. They grow rapidly and require spacious tanks.",
        "emoji": "🐡",
        "color": "#10b981"
    },
}


def get_fish_info(species_name: str) -> dict:
    """Get detailed information about a fish species."""
    return FISH_DATABASE.get(species_name, None)


def get_all_species() -> list:
    """Return a list of all classified species."""
    return list(FISH_DATABASE.keys())


def get_species_colors() -> dict:
    """Return a mapping of species to their theme colors."""
    return {name: info["color"] for name, info in FISH_DATABASE.items()}
