from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

root = Path('/home/ubuntu/forest_carousel/2026-11-25')
font_path = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
root.mkdir(parents=True, exist_ok=True)

cards = {
'224490376217': [
 ('겨울 숲 프로그램,\n“무료·영유아”만 보고\n신청해도 될까?', '목록 표시는 시작점이야'),
 ('무료·겨울·영유아\n목록에서 먼저\n확인할 정보', '참가비·계절·대상 범주'),
 ('영유아 표시는\n0~5세 기준이지만', '회차별 세부 연령은 따로 확인해'),
 ('신청 전에는\n날짜·장소·정원·모집 상태', '상세 화면에서 차례로 봐'),
 ('오늘 할 일\n프로그램 이름을 눌러\n상세 조건까지 확인하기', '목록 한 줄로 결정하지 않기'),
],
'224489666934': [
 ('숲 체험 뒤\n아이 양말이 젖었다면\n어떻게 하지?', '여벌 한 켤레가 일을 줄여줘'),
 ('깨끗한 여벌 양말은\n작은 파우치에', '가방 바닥 말고 바로 찾는 곳에'),
 ('사용한 양말은\n봉투에 따로', '깨끗한 양말과 섞이지 않게'),
 ('아이에게 미리 알려줘\n“양말은 이 주머니야”', '필요할 때 스스로 찾기 쉬워'),
 ('오늘 가방에\n여벌 양말과 봉투\n넣어두기', '작은 준비 하나면 충분해'),
],
'224489244908': [
 ('“무료·가을·영유아”\n표시만 보면\n신청할 수 있을까?', '목록과 실제 회차는 달라'),
 ('무료·가을·대상\n목록은 후보를\n고르는 정보', '상세 조건을 대신하진 않아'),
 ('운영일과 장소\n접수 상태를\n먼저 확인해', '원하는 날짜에 열리는지 보기'),
 ('세부 연령·동반 여부\n준비물·비용도', '신청 전에 한 번 더 맞춰봐'),
 ('오늘 할 일\n관심 프로그램을 열고\n4가지만 체크하기', '날짜·장소·접수·대상'),
],
}

palettes = [('#26483b','#f3e6bb'),('#315c4b','#f7e8bd'),('#486b54','#fff0c7'),('#6b7047','#fff4d2'),('#24483b','#e7c77e')]

def wrap(draw, text, font, max_width):
    out=[]
    for para in text.split('\n'):
        cur=''
        for ch in para:
            if cur and draw.textbbox((0,0), cur+ch, font=font)[2] > max_width:
                out.append(cur); cur=ch
            else:
                cur += ch
        out.append(cur)
    return out

def centered(draw, text, y, font, fill, max_width=900, spacing=16):
    lines=wrap(draw,text,font,max_width)
    heights=[draw.textbbox((0,0), line, font=font)[3] for line in lines]
    total=sum(heights)+spacing*(len(lines)-1)
    yy=y-total/2
    for line,h in zip(lines,heights):
        box=draw.textbbox((0,0),line,font=font)
        x=(1080-(box[2]-box[0]))/2
        draw.text((x,yy),line,font=font,fill=fill)
        yy += h+spacing

for slug, slides in cards.items():
    out=root/slug; out.mkdir(parents=True, exist_ok=True)
    for i,(main,sub) in enumerate(slides,1):
        bg, accent=palettes[i-1]
        im=Image.new('RGB',(1080,1080),bg)
        d=ImageDraw.Draw(im)
        title=ImageFont.truetype(font_path,68)
        body=ImageFont.truetype(font_path,42)
        small=ImageFont.truetype(font_path,28)
        d.ellipse((790,-120,1180,270), fill=accent)
        for x,y,r in [(120,180,12),(180,240,8),(930,430,10),(860,520,6),(210,820,9)]:
            d.ellipse((x-r,y-r,x+r,y+r), fill=accent)
        d.arc((90,620,520,1030),190,350,fill=accent,width=5)
        d.line((110,900,480,650),fill=accent,width=5)
        for x,y in [(260,790),(310,755),(360,720),(410,685)]:
            d.ellipse((x-10,y-10,x+10,y+10),fill=accent)
        d.text((72,70),f'{i:02d}  생각하는 숲',font=small,fill=accent)
        centered(d,main,430,title,accent)
        centered(d,sub,790,body,'#ffffff' if i in (1,5) else accent,850,12)
        d.text((72,995),'아이의 속도로 살펴보는 숲 이야기',font=small,fill=accent)
        im.save(out/f'{i:02d}.png', format='PNG', optimize=True)
print(root)
