import yt_dlp

def get_video_info(search_text):
    # خيارات البحث في yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best', # نختار أفضل جودة صوت
        'noplaylist': True,          # نأخذ فيديو واحد مش قائمة تشغيل
        'quiet': True,              # ما تطبعش تفاصيل كثيرة في الـ Terminal
    }
    
    # الكلمة "ytsearch1:" بتخلي yt-dlp يبحث ويرجع نتيجة واحدة بس
    search_query = f"ytsearch1:{search_text}"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # extract_flat=False بيجيب كل المعلومات بما فيها رابط البث المباشر (url)
        info = ydl.extract_info(search_query, download=False)
        
        if 'entries' in info and len(info['entries']) > 0:
            first_result = info['entries'][0]
            
            return {
                'id': first_result.get('id'),
                'title': first_result.get('title'),
                'stream_url': first_result.get('url'), # رابط الصوت المباشر
            }
            
    return None