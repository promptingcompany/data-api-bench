# Monid image-to-video price snapshot, 2026-11-17 12:47 SF (key tpc-e3-build)
5 s clip, >=720p, keeps 9:16 from a 9:16 input image
1. heygen /promo/v1/video/heygen-video-1-i2v  768p $0.018/s = $0.09  (promo, 50% off, through 2026-11-30; 10/min 100/h 300/day per workspace)
2. heygen /v1/video/heygen-video-1-i2v        768p $0.036/s = $0.18
3. kling  /v1/video/kling-2.5-turbo-i2v       720p $0.042/s = $0.21  (silent)
3. kling  /v1/video/kling-2.6-i2v             720p audio off $0.042/s = $0.21
5. bytedance /v1/video/seedance-2.0-mini      720p ~108k tokens x $3.5/M = ~$0.38
6. minimax /v1/video/minimax-h3               768P $0.08/s = $0.40
7. kling 4.0-flash-i2v $0.47; wan2.7-i2v $0.50; gemini omni-flash-i2v $0.55 (degraded)
Raw: discovery/*.json, discovery/inspect/*.json
