from models import Profile, Post, ProfileStats, PostType, ContentCategory
import random

def create_mock_profile(archetype: str) -> Profile:
    """
    Generates a mock profile based on an archetype:
    - 'spammer': High sales content, low engagement.
    - 'ghost': Low frequency, random content.
    - 'leader': Balanced content, high authority.
    """
    
    posts = []
    
    if archetype == "spammer":
        handle = "@tienda_desesperada"
        name = "Tienda de Cosas Varias"
        bio = "COMPRA AQUÍ 👇 ENVIOS A TODO EL PAIS. OFERTAS!!! 📦"
        pic = "https://ui-avatars.com/api/?name=Tienda+X&background=random"
        
        # 9 posts, mostly sales
        for i in range(1, 10):
            posts.append(Post(
                id=f"post_{i}",
                type=PostType.STATIC,
                caption=f"OFERTA RELÁMPAGO solo por hoy! Compra ya el producto {i}. Link en bio. #oferta #venta #compra",
                likes=random.randint(2, 15),
                comments=0,
                category=ContentCategory.SALES,
                image_url=f"https://placehold.co/400x400?text=Producto+{i}"
            ))
            
        stats = ProfileStats(
            total_posts=150,
            followers=450,
            following=2000,
            engagement_rate=0.5,
            posts_per_week=10.0
        )

    elif archetype == "ghost":
        handle = "@creador_fantasma"
        name = "Juan Pérez"
        bio = "A veces subo cosas. 🤷‍♂️"
        pic = "https://ui-avatars.com/api/?name=Juan+Perez&background=gray"
        
        # 3 posts, very spread out
        caps = ["Feliz año...", "En la playa", "Foto de mi gato"]
        for i, cap in enumerate(caps):
            posts.append(Post(
                id=f"post_{i}",
                type=PostType.STATIC,
                caption=cap,
                likes=random.randint(30, 50),
                comments=2,
                category=ContentCategory.FILLER,
                image_url=f"https://placehold.co/400x400?text=Foto+{i}"
            ))
            
        stats = ProfileStats(
            total_posts=12,
            followers=800,
            following=300,
            engagement_rate=3.0,
            posts_per_week=0.2
        )

    else: # leader
        handle = "@estratega_top"
        name = "Sofia | Marketing"
        bio = "Te ayudo a escalar tu negocio sin estrés. ✨ +10k alumnos."
        pic = "https://ui-avatars.com/api/?name=Sofia+M&background=0D8ABC&color=fff"
        
        types = [
            (PostType.REEL, ContentCategory.EDUCATIONAL, "3 Errores que matan tu alcance 🚀...\n(Lee la descripción)"),
            (PostType.STATIC, ContentCategory.PERSONAL_BRAND, "La verdad es que ayer quise renunciar. Te cuento por qué..."),
            (PostType.CAROUSEL, ContentCategory.EDUCATIONAL, "Guía paso a paso para tu estrategia 2025."),
            (PostType.STATIC, ContentCategory.OPINION, "Dejen de usar bots. Es vergonzoso."),
            (PostType.REEL, ContentCategory.SALES, "Últimos lugares para el workshop. ¿Te sumas?"),
            (PostType.STATIC, ContentCategory.DOCUMENTARY, "Backstage de la grabación de hoy 🎥"),
        ]
        
        for i, (ptype, cat, cap) in enumerate(types):
            posts.append(Post(
                id=f"post_{i}",
                type=ptype,
                caption=cap,
                likes=random.randint(150, 500),
                comments=random.randint(20, 80),
                category=cat,
                image_url=f"https://placehold.co/400x400?text=Contenido+{cat.name}"
            ))

        stats = ProfileStats(
            total_posts=340,
            followers=12500,
            following=150,
            engagement_rate=4.5,
            posts_per_week=4.0
        )

    return Profile(
        handle=handle,
        name=name,
        bio=bio,
        profile_pic_url=pic,
        stats=stats,
        posts=posts
    )
