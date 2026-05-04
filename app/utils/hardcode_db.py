from app.models import Song
from app.extensions import db
import logging
songs=[
    {
        "song_id": 1116333465,
        "title": "Aa Zara",
        "artist": "Sunidhi Chauhan",
        "album": "Murder 2 (Original Motion Picture Soundtrack)",
        "preview": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview221/v4/92/65/d1/9265d1e0-b19b-4ccd-4b35-95d23bb6f62b/mzaf_14951350143201301935.plus.aac.p.m4a",
        "image": "https://is1-ssl.mzstatic.com/image/thumb/Music114/v4/bb/cc/4b/bbcc4bd9-b705-8cff-d637-6379ac87b9a6/8902894695916_cover.jpg/60x60bb.jpg"
    },
    {
        "song_id": 1070912823,
        "title": "Dilliwaali Girlfriend",
        "artist": "Pritam, Arijit Singh & Sunidhi Chauhan",
        "album": "Yeh Jawaani Hai Deewani (Original Motion Picture Soundtrack)",
        "preview": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview211/v4/95/f6/5f/95f65f13-4a42-6b9a-2689-0b221473ea3b/mzaf_12878159079636166594.plus.aac.p.m4a",
        "image": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/62/d6/74/62d67432-0670-631f-db6a-d4bac3adae4b/8902894353328_cover.jpg/60x60bb.jpg"
    },
    {
        "song_id": 1115905461,
        "title": "Kashmir Main Tu Kanyakumari",
        "artist": "Sunidhi Chauhan, Arijit Singh & Neeti Mohan",
        "album": "Chennai Express (Original Motion Picture Soundtrack)",
        "preview": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview115/v4/88/5d/70/885d7075-0aa3-4f0d-1ad8-bbd9beb470e3/mzaf_15376495732266340804.plus.aac.p.m4a",
        "image": "https://is1-ssl.mzstatic.com/image/thumb/Music124/v4/91/89/89/918989bc-cc33-5538-cd16-76f400aab629/8902894353823_cover.jpg/60x60bb.jpg"
    },
    {
        "song_id": 1440936036,
        "title": "Wildest Dreams",
        "artist": "Taylor Swift",
        "album": "1989",
        "preview": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview211/v4/d0/91/84/d0918464-ed0d-eed2-89bd-1d3b2ebe85c5/mzaf_5128468383438758741.plus.aac.p.m4a",
        "image": "https://is1-ssl.mzstatic.com/image/thumb/Music221/v4/89/4a/4a/894a4ab9-b0b0-9ea5-ca41-8da0b9b79453/14UMDIM03405.rgb.jpg/60x60bb.jpg"
    },
    {
        "song_id": 1468058173,
        "title": "Lover",
        "artist": "Taylor Swift",
        "album": "Lover",
        "preview": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview211/v4/e0/db/47/e0db47b0-7f70-0631-0414-cd4777d2fb3e/mzaf_6362891154838442638.plus.aac.p.m4a",
        "image": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/49/3d/ab/493dab54-f920-9043-6181-80993b8116c9/19UMGIM53909.rgb.jpg/60x60bb.jpg"
    },
    {
        "song_id": 1468448742,
        "title": "Tujhe Kitna Chahne Lage",
        "artist": "Arijit Singh",
        "album": "Kabir Singh (Original Motion Picture Soundtrack)",
        "preview": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview221/v4/16/6b/75/166b752b-c288-d978-54f2-ae6bb8368346/mzaf_8053064283423859432.plus.aac.p.m4a",
        "image": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/f6/70/84/f6708434-0123-ff36-0ac3-7401e8cf0f94/8902894360807_cover.jpg/60x60bb.jpg"
    },
    {
        "song_id": 1694486810,
        "title": "Tum Kya Mile (From 'Rocky Aur Rani Kii Prem Kahaani')",
        "artist": "Pritam, Arijit Singh, Shreya Ghoshal & Amitabh Bhattacharya",
        "album": "Tum Kya Mile (From 'Rocky Aur Rani Kii Prem Kahaani') - Single",
        "preview": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview211/v4/22/f8/f1/22f8f120-e3cb-31ed-2bf5-b217c1b17873/mzaf_15170293722669283908.plus.aac.p.m4a",
        "image": "https://is1-ssl.mzstatic.com/image/thumb/Music116/v4/d9/40/f5/d940f50f-07f3-4419-a6a0-d8f631f512f6/197189253423.jpg/60x60bb.jpg"
    },
    {
        "song_id": 1324456545,
        "title": "Dil Diyan Gallan",
        "artist": "Vishal & Shekhar & Atif Aslam",
        "album": "Tiger Zinda Hai (Original Motion Picture Soundtrack)",
        "preview": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview221/v4/70/5a/67/705a67b0-a61f-db2c-bb6a-ab06c78a4386/mzaf_5706499000965104644.plus.aac.p.m4a",
        "image": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/55/16/15/5516155a-733c-800c-1081-e5e982e8a603/849486091696_cover.jpg/60x60bb.jpg"
    }
]

def seed_songs():
    for s in songs :
        existing=Song.query.filter_by(song_id=s["song_id"]).first()

        if not existing :
            song=Song(
                song_id=s["song_id"],
                title=s["title"],
                artist=s["artist"],
                album=s["album"],
                image=s["image"],
                preview=s["preview"]
            )
            db.session.add(song)
    db.session.commit()
    logging.info(f"Seed songs added succesfully!")