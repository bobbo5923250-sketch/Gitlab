# AI Engineer Portfolio

Personal portfolio website — plain HTML, CSS and JavaScript, no build step. Ready for GitHub Pages.

## วิธีแก้ข้อมูล

แก้ไฟล์ [`data.js`](data.js) ไฟล์เดียว: ชื่อ, ตำแหน่ง, ทักษะ, โปรเจกต์, ประสบการณ์, ช่องทางติดต่อ

- โปรเจกต์ที่ตั้ง `featured: true` จะแสดงก่อนและมีป้าย "featured"
- ปุ่มกรองโปรเจกต์สร้างจาก `tags` ให้อัตโนมัติ
- ถ้ามีไฟล์ resume ให้วาง `resume.pdf` ในโฟลเดอร์นี้ แล้วตั้ง `resumeUrl: "resume.pdf"`

## ดูบนเครื่อง

เปิด `index.html` ในเบราว์เซอร์ได้เลย หรือรัน

```bash
python -m http.server 8000
# แล้วเปิด http://localhost:8000
```

## เอาขึ้น GitHub Pages

1. สร้าง repo ใหม่ชื่อ `<your-username>.github.io` บน GitHub (ใช้ชื่อนี้เว็บจะอยู่ที่ `https://<your-username>.github.io`)
2. Push ไฟล์ในโฟลเดอร์นี้ขึ้นไป:

   ```bash
   git init
   git add .
   git commit -m "Initial portfolio"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<your-username>.github.io.git
   git push -u origin main
   ```

3. ไปที่ **Settings → Pages** แล้วเลือก Source เป็น `Deploy from a branch`, branch `main`, โฟลเดอร์ `/ (root)`
4. รอ 1–2 นาที เว็บก็จะออนไลน์

## เคล็ดลับให้ portfolio ดูดีสำหรับตำแหน่ง AI Engineer

- ใส่ตัวเลขผลลัพธ์จริงในแต่ละโปรเจกต์ (accuracy, latency, ต้นทุนที่ลดได้)
- ให้ทุกโปรเจกต์มีลิงก์ repo ที่มี README ดี ๆ และถ้าทำได้ ให้มี live demo (เช่น Hugging Face Spaces, Streamlit)
- เลือกโปรเจกต์เด่นแค่ 3–6 ชิ้น เน้นคุณภาพมากกว่าจำนวน
