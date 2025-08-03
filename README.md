# PSU Note - แอปพลิเคชันบันทึกโน้ตอัจฉริยะ

แอปพลิเคชัน PSU Note เป็นระบบจัดการโน้ตและแท็กที่ทันสมัย พัฒนาด้วย Flask และ PostgreSQL สำหรับการจัดเก็บ จัดระเบียบ และค้นหาข้อความสำคัญอย่างมีประสิทธิภาพ ด้วยอินเทอร์เฟซที่ใช้งานง่ายและระบบแท็กที่ยืดหยุ่น

## คุณสมบัติหลัก

- **การจัดการโน้ตแบบครบวงจร**: สร้าง แก้ไข และลบโน้ตได้อย่างสะดวกรวดเร็ว
- **ระบบแท็กอัจฉริยะ**: สร้าง แก้ไข และลบแท็กเพื่อจัดหมวดหมู่โน้ตอย่างเป็นระบบ
- **ความสัมพันธ์แบบหลายต่อหลาย**: โน้ตหนึ่งรายการสามารถมีได้หลายแท็ก และแท็กหนึ่งสามารถใช้กับโน้ตได้หลายรายการ
- **ติดตามการเปลี่ยนแปลง**: แสดงเวลาล่าสุดที่โน้ตถูกแก้ไขพร้อมประวัติการปรับปรุง
- **การกรองและค้นหา**: แสดงโน้ตที่เกี่ยวข้องกับแท็กที่เลือกได้อย่างรวดเร็ว
- **อินเทอร์เฟซที่ใช้งานง่าย**: ออกแบบด้วย Bootstrap 5 เพื่อประสบการณ์การใช้งานที่ดี

## ฟีเจอร์ใหม่ที่เพิ่มเข้ามา

- **ระบบการแจ้งเตือน**: แจ้งเตือนเมื่อมีการสร้าง แก้ไข หรือลบโน้ตและแท็ก
- **การค้นหาขั้นสูง**: ค้นหาโน้ตตามหัวข้อ เนื้อหา หรือแท็กได้อย่างรวดเร็ว
- **การจัดการแบบแบทช์**: เลือกและจัดการโน้ตหลายรายการพร้อมกัน
- **ระบบการแบ่งหน้า**: รองรับการแสดงผลโน้ตจำนวนมากอย่างมีประสิทธิภาพ

## โครงสร้างโปรเจค

```
postgresql/
├── docker-compose.yml       # ไฟล์กำหนดค่า Docker สำหรับ PostgreSQL และ pgAdmin
├── requirements.txt         # รายการ dependencies หลักของโปรเจค
├── README.md               # เอกสารนี้
└── psunote/               # โฟลเดอร์แอปพลิเคชันหลัก
    ├── models.py          # โมเดลฐานข้อมูล (Note, Tag, ความสัมพันธ์)
    ├── forms.py           # แบบฟอร์ม WTForms สำหรับการรับข้อมูล
    ├── noteapp.py         # แอปพลิเคชัน Flask หลักและ routing
    ├── templates/         # เทมเพลตเพจ HTML ด้วย Jinja2
    │   ├── base.html      # เทมเพลตหลักที่ใช้ร่วมกัน
    │   ├── index.html     # หน้าแรกแสดงรายการโน้ตทั้งหมด
    │   ├── notes-create.html  # ฟอร์มสร้างโน้ตใหม่
    │   ├── notes-edit.html    # ฟอร์มแก้ไขโน้ต
    │   ├── notes-delete.html  # หน้ายืนยันการลบโน้ต
    │   ├── tags-create.html   # ฟอร์มสร้างแท็กใหม่
    │   ├── tags-edit.html     # ฟอร์มแก้ไขแท็ก
    │   ├── tags-delete.html   # หน้ายืนยันการลบแท็ก
    │   └── tags-view.html     # หน้าแสดงโน้ตตามแท็กที่เลือก
    └── __pycache__/       # ไฟล์ bytecode ที่ Python สร้างขึ้น
```

## การติดตั้งและการตั้งค่า

### การใช้ Docker 

1. **ติดตั้ง Docker และ Docker Compose**

   - สำหรับ Windows: ดาวน์โหลด Docker Desktop จาก [docker.com](https://www.docker.com/products/docker-desktop)
   - สำหรับ Linux/Mac: ติดตั้งตามคำแนะนำใน [เอกสาร Docker](https://docs.docker.com/get-docker/)
2. **เริ่มต้นฐานข้อมูล PostgreSQL และ pgAdmin**

   ```bash
   # เปิด Terminal/Command Prompt ที่โฟลเดอร์โปรเจค
   cd postgresql

   # เริ่มต้นบริการ PostgreSQL และ pgAdmin
   docker-compose up -d
   ```
3. **ตรวจสอบสถานะการทำงาน**

   ```bash
   # ตรวจสอบว่าบริการทำงานปกติหรือไม่
   docker-compose ps
   ```
4. **การเข้าถึงบริการ**

   - **PostgreSQL Database**: `localhost:5432`
     - Database: `coedb`
     - Username: `coe`
     - Password: `CoEpasswd`
   - **pgAdmin Web Interface**:
     - HTTP: `http://localhost:7080`
     - HTTPS: `https://localhost:7443`
     - Email: `coe@local.db`
     - Password: `CoEpasswd`

#### การตั้งค่าผ่าน pgAdmin (ถ้าใช้ Docker)

1. เปิดเว็บเบราว์เซอร์ไปที่ `http://localhost:7080`
2. เข้าสู่ระบบด้วย:
   - Email: `coe@local.db`
   - Password: `CoEpasswd`
3. เพิ่มเซิร์ฟเวอร์ใหม่:
   - Name: `PostgreSQL Local`
   - Host: `postgresql` (ชื่อ container)
   - Port: `5432`
   - Username: `coe`
   - Password: `CoEpasswd`

### การเริ่มต้นใช้งานแอปพลิเคชัน

1. **เข้าไปในโฟลเดอร์แอปพลิเคชัน**

   ```bash
   cd psunote
   ```
2. **เริ่มต้นแอปพลิเคชัน Flask**

   ```bash
   # ถ้าใช้ virtual environment (วิธีที่ 2)
   python noteapp.py

   # หรือถ้าใช้ Docker สามารถรันแอปได้โดยตรง
   python noteapp.py
   ```
3. **เปิดเว็บเบราว์เซอร์และไปที่**

   ```
   http://localhost:5000
   ```

### การจัดการ Docker Services

```bash
# เริ่มต้นบริการ
docker-compose up -d

# หยุดบริการ
docker-compose stop

# หยุดและลบ containers
docker-compose down

# ดูสถานะบริการ
docker-compose ps

# ดู logs
docker-compose logs postgresql
docker-compose logs pgadmin

# เข้าไปใน PostgreSQL container
docker-compose exec postgresql psql -U coe -d coedb
```

## Dependencies และ Requirements

### requirements.txt

```
flask              # เฟรมเวิร์คเว็บ Python
flask-wtf          # การจัดการฟอร์มใน Flask
flask-sqlalchemy   # ORM สำหรับฐานข้อมูล
wtforms-sqlalchemy # การผสานระหว่าง WTForms และ SQLAlchemy
psycopg2-binary    # PostgreSQL adapter สำหรับ Python
```

### Docker Services

- **PostgreSQL 15**: ระบบจัดการฐานข้อมูลหลัก
- **pgAdmin 4**: เครื่องมือจัดการฐานข้อมูล PostgreSQL ผ่านเว็บ

## วิธีการใช้งาน

### การจัดการโน้ต

- **สร้างโน้ตใหม่**: คลิกปุ่ม "สร้างโน้ตใหม่" ที่หน้าแรก กรอกข้อมูลและแท็กที่เกี่ยวข้อง (คั่นด้วยเครื่องหมายจุลภาค)
- **แก้ไขโน้ต**: คลิกปุ่ม "แก้ไข" บนการ์ดโน้ตที่ต้องการ
- **ลบโน้ต**: คลิกปุ่ม "ลบ" บนการ์ดโน้ตและยืนยันการลบ

### การจัดการแท็ก

- **สร้างแท็กใหม่**: คลิกปุ่ม "สร้าง Tag ใหม่" ที่หน้าแรก
- **ดูโน้ตตามแท็ก**: คลิกที่แท็กใดๆ ในโน้ตเพื่อแสดงโน้ตทั้งหมดที่มีแท็กนั้น
- **แก้ไขแท็ก**: ไปที่หน้าแสดงโน้ตตามแท็กและคลิกปุ่ม "แก้ไข"
- **ลบแท็ก**: ไปที่หน้าแสดงโน้ตตามแท็กและคลิกปุ่ม "ลบ"

## เทคโนโลยีที่ใช้

- **Backend**: Flask, SQLAlchemy, Flask-WTF
- **Database**: PostgreSQL 15
- **Frontend**: Bootstrap 5, HTML5, Jinja2 
- **Form Handling**: Flask-WTF, WTForms
- **Database ORM**: SQLAlchemy
- **Containerization**: Docker, Docker Compose
- **Database Management**: pgAdmin 4

## ผู้พัฒนา

พัฒนาโดย 6510110541 นายอับดาร์ เอียดวารี สำหรับ 241-353 ART INTELL ECOSYSTEM MODULE  สาขาวิชาวิศวกรรมปัญญาประดิษฐ์ มหาวิทยาลัยสงขลานครินทร์
