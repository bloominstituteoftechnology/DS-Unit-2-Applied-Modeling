import numpy as np
import pandas as pd

def fix_related(cell):
    classes = ['Alternative version','Prequel','Other','Sequel','Adaptation','Full story',
               'Parent story','Summary','Side story','Character','Spin-off','Alternative setting']
    x = []
    if cell == '[]':
        return 'None'
    
    for i in classes:
        if i in cell:
            x.append(i)
    if len(x) > 0:
        return ','.join(x)
    else:
        return np.nan
    
def num_rel(cell):
    if cell == 'None':
        return 0
    else:
        return len(cell.split(','))
    
def duration(cell):
    temp = cell.strip('.').split('. ')
    temp = temp[0]
    if temp == 'Unknown':
        return np.nan
    elif 'hr' in temp:
        return '60+'
    elif 'sec' in temp:
        return 'less than a minute'
    else:
        time = int(temp.split()[0])
        if 30 < time < 60:
            return '31-59'
        elif 20 < time <= 30:
            return '21-30'
        else:
            return '1-20'
        
def studio(data):
    
    studios = ['Toei Animation','Sunrise','J.C.Staff',
           'Madhouse','Production I.G','TMS Entertainment',
           'Studio Deen','Studio Pierrot','Nippon Animation']
    
    if data not in studios:
        return 'other'
    else:
        return data

def encode_target(cell):
    x = 2553.6
    if cell <= x:
        return 'Really good'
    elif cell <= x*2:
        return 'OK'
    elif cell <= x*3:
        return 'Questionable'
    else:
        return 'Bad'

def wrangle(data):
    
    #setting with copy warning
    df = data.copy()
    #Some dropping
    col_drop = [
        'title_english','title_japanese','title_synonyms','image_url',
        'opening_theme','ending_theme','anime_id','background','premiered',
        'broadcast','producer','licensor','aired_string','aired','score',
        'scored_by','members','favorites','status','airing'
        ]

    df.drop(col_drop,axis=1,inplace=True)
    # making related useable
    df.related = df.related.apply(fix_related)
    # Feature engineer
    df['num_related'] = df.related.apply(num_rel)
    # fixing cardinality
    df.genre.replace(np.nan,'unknown',inplace=True)
    
    hentai = ['Yaoi','Yuri','Ecchi','Harem','Hentai','Josei','Shounen Ai','Shoujo Ai','Romance']
    sports = ['Martial Arts','Sports']
    youth = ['Kids','Seinen','Shoujo','Shounen','Super Power','Slice of Life','School','Action']
    adv_psych = ['Adventure','Mystery','Psychological','Dementia']
    drama_thrill = ['Drama','Horror','Thriller']
    fant_scien = ['Demons','Fantasy','Game','Magic','Supernatural','Vampire','Sci-Fi','Cars','Space']
    comedy = ['Comedy','Parody']
    military = ['Military','Police','Mecha']
    misc = ['Historical','Samurai','Music']

    df['hentai/romance'] = df.genre.str.contains('|'.join(hentai))
    df['sports'] = df.genre.str.contains('|'.join(sports))
    df['youth'] = df.genre.str.contains('|'.join(youth))
    df['adventure/psychological'] = df.genre.str.contains('|'.join(adv_psych))
    df['drama'] = df.genre.str.contains('|'.join(drama_thrill))
    df['fantasy/sci-fi'] = df.genre.str.contains('|'.join(fant_scien))
    df['comedy'] = df.genre.str.contains('|'.join(comedy))
    df['military'] = df.genre.str.contains('|'.join(military))
    df['misc'] = df.genre.str.contains('|'.join(misc))
    df['Unknown'] = df.genre.str.contains('unknown')
    # More dropping
    df.drop(['genre','related','title'],axis=1,inplace=True)
    df.drop([8397,14005,14067,14074,14106,14184,14227,14277,14408],inplace=True)
    # making duration useable
    df.duration = df.duration.apply(duration)
    #fix studio
    df.studio = df.studio.apply(studio)
    #more dropping
    df.drop(df[df['rank'].isnull()].index, inplace=True)
    df.dropna(inplace=True)
    #make target
    df['target'] = (df['rank'] + df['popularity']) / 2
    df['class'] = df['target'].apply(encode_target)
    #drop leakage
    df.drop(['rank','popularity','target'],axis=1,inplace=True)
    return df



if __name__ == '__main__':
    wrangle(df)