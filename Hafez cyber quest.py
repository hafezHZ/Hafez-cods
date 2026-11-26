
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import random
from datetime import datetime

# ==========================================
# ماجراجویی سایبری حافظ
# HAFEZ CYBER QUEST - Persian Edition
# ==========================================

APP_NAME = "ماجراجویی سایبری حافظ"
APP_VERSION = "2.0"
DATA_FILE = "hafez_cyber_data.json"

BG = "#080D18"
PANEL = "#111B2D"
PANEL_LIGHT = "#17243A"
ACCENT = "#00E5FF"
GOLD = "#FFD166"
GREEN = "#00E676"
RED = "#FF5252"
WHITE = "#F4F7FF"
MUTED = "#8B9BB4"

DEFAULT_DATA = {
    "username": "بازیکن حافظ",
    "level": 1,
    "xp": 0,
    "coins": 100,
    "completed": [],
    "inventory": [],
    "achievements": [],
    "settings": {
        "sound": True,
        "notifications": True
    },
    "created": datetime.now().strftime("%Y-%m-%d")
}


class HafezCyberQuest:

    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("1200x760")
        self.root.minsize(950, 600)
        self.root.configure(bg=BG)

        self.data = self.load_data()
        self.current_page = "خانه"
        self.missions = self.create_missions()

        self.setup_styles()
        self.create_layout()
        self.show_dashboard()
        self.update_clock()

    # ------------------------------------------
    # ذخیره و بارگذاری
    # ------------------------------------------

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as file:
                    saved = json.load(file)

                data = DEFAULT_DATA.copy()
                data.update(saved)

                if "settings" not in data:
                    data["settings"] = DEFAULT_DATA["settings"].copy()

                return data

            except Exception:
                return DEFAULT_DATA.copy()

        return DEFAULT_DATA.copy()

    def save_data(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as file:
                json.dump(
                    self.data,
                    file,
                    ensure_ascii=False,
                    indent=4
                )
        except Exception as error:
            messagebox.showerror(
                "خطای ذخیره‌سازی",
                str(error)
            )

    # ------------------------------------------
    # تنظیمات ظاهری
    # ------------------------------------------

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Quest.Horizontal.TProgressbar",
            troughcolor=PANEL_LIGHT,
            background=ACCENT,
            bordercolor=PANEL_LIGHT,
            lightcolor=ACCENT,
            darkcolor=ACCENT
        )

    def create_layout(self):
        self.main_frame = tk.Frame(
            self.root,
            bg=BG
        )
        self.main_frame.pack(
            fill="both",
            expand=True
        )

        self.sidebar = tk.Frame(
            self.main_frame,
            bg=PANEL,
            width=230
        )
        self.sidebar.pack(
            side="right",
            fill="y"
        )
        self.sidebar.pack_propagate(False)

        self.content = tk.Frame(
            self.main_frame,
            bg=BG
        )
        self.content.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.create_sidebar()
        self.create_topbar()

    # ------------------------------------------
    # منوی کناری
    # ------------------------------------------

    def create_sidebar(self):
        logo = tk.Label(
            self.sidebar,
            text="⚡ حافظ",
            bg=PANEL,
            fg=ACCENT,
            font=("Tahoma", 24, "bold")
        )
        logo.pack(pady=(30, 5))

        subtitle = tk.Label(
            self.sidebar,
            text="ماجراجویی سایبری",
            bg=PANEL,
            fg=MUTED,
            font=("Tahoma", 10)
        )
        subtitle.pack(pady=(0, 25))

        menu_items = [
            ("🏠", "خانه"),
            ("🎯", "مأموریت‌ها"),
            ("🛒", "فروشگاه"),
            ("🎒", "کوله‌پشتی"),
            ("🏆", "دستاوردها"),
            ("👤", "پروفایل"),
            ("📊", "رتبه‌بندی"),
            ("⚙️", "تنظیمات")
        ]

        self.menu_buttons = {}

        for icon, title in menu_items:
            button = tk.Button(
                self.sidebar,
                text=f"{icon}   {title}",
                command=lambda page=title: self.navigate(page),
                bg=PANEL,
                fg=WHITE,
                activebackground=PANEL_LIGHT,
                activeforeground=ACCENT,
                font=("Tahoma", 11),
                relief="flat",
                bd=0,
                anchor="e",
                padx=22,
                pady=13,
                cursor="hand2"
            )
            button.pack(fill="x", padx=10, pady=2)
            self.menu_buttons[title] = button

        tk.Frame(
            self.sidebar,
            bg=PANEL_LIGHT,
            height=1
        ).pack(fill="x", padx=18, pady=20)

        self.sidebar_status = tk.Label(
            self.sidebar,
            text="● سیستم آماده است",
            bg=PANEL,
            fg=GREEN,
            font=("Tahoma", 9)
        )
        self.sidebar_status.pack(pady=10)

    # ------------------------------------------
    # نوار بالایی
    # ------------------------------------------

    def create_topbar(self):
        self.topbar = tk.Frame(
            self.content,
            bg=PANEL,
            height=75
        )
        self.topbar.pack(fill="x")
        self.topbar.pack_propagate(False)

        self.page_title = tk.Label(
            self.topbar,
            text="خانه",
            bg=PANEL,
            fg=WHITE,
            font=("Tahoma", 17, "bold")
        )
        self.page_title.pack(
            side="right",
            padx=25
        )

        self.clock_label = tk.Label(
            self.topbar,
            text="",
            bg=PANEL,
            fg=MUTED,
            font=("Tahoma", 10)
        )
        self.clock_label.pack(
            side="left",
            padx=25
        )

    # ------------------------------------------
    # ابزارهای رابط کاربری
    # ------------------------------------------

    def clear_content(self):
        for widget in self.content.winfo_children():
            if widget != self.topbar:
                widget.destroy()

    def make_label(
        self,
        parent,
        text,
        size=12,
        color=WHITE,
        bold=False
    ):
        return tk.Label(
            parent,
            text=text,
            bg=parent.cget("bg"),
            fg=color,
            font=(
                "Tahoma",
                size,
                "bold" if bold else "normal"
            ),
            anchor="e",
            justify="right"
        )

    def make_card(self, parent, title, value, color=ACCENT):
        card = tk.Frame(
            parent,
            bg=PANEL,
            padx=20,
            pady=18
        )

        tk.Label(
            card,
            text=title,
            bg=PANEL,
            fg=MUTED,
            font=("Tahoma", 10)
        ).pack(anchor="e")

        tk.Label(
            card,
            text=value,
            bg=PANEL,
            fg=color,
            font=("Tahoma", 21, "bold")
        ).pack(anchor="e", pady=(10, 0))

        return card

    # ------------------------------------------
    # ساعت برنامه
    # ------------------------------------------

    def update_clock(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.clock_label.config(
            text=f"ساعت سیستم: {now}"
        )
        self.root.after(1000, self.update_clock)

    # ------------------------------------------
    # صفحه اصلی
    # ------------------------------------------

    def show_dashboard(self):
        self.clear_content()
        self.current_page = "خانه"
        self.page_title.config(text="خانه")

        container = tk.Frame(
            self.content,
            bg=BG,
            padx=30,
            pady=25
        )
        container.pack(fill="both", expand=True)

        welcome = tk.Label(
            container,
            text=f"خوش آمدی، {self.data['username']}!",
            bg=BG,
            fg=WHITE,
            font=("Tahoma", 22, "bold"),
            anchor="e"
        )
        welcome.pack(fill="x", pady=(10, 5))

        description = tk.Label(
            container,
            text="آماده‌ای وارد دنیای مأموریت‌های سایبری شوی؟",
            bg=BG,
            fg=MUTED,
            font=("Tahoma", 11),
            anchor="e"
        )
        description.pack(fill="x", pady=(0, 25))

        stats = tk.Frame(container, bg=BG)
        stats.pack(fill="x", pady=10)

        cards = [
            ("⭐ سطح", str(self.data["level"]), GOLD),
            ("🪙 سکه‌ها", str(self.data["coins"]), ACCENT),
            ("⚡ تجربه", str(self.data["xp"]), GREEN),
            ("🎯 مأموریت‌ها", str(len(self.data["completed"])), WHITE)
        ]

        for title, value, color in cards:
            card = self.make_card(
                stats,
                title,
                value,
                color
            )
            card.pack(
                side="right",
                fill="both",
                expand=True,
                padx=6
            )

        tk.Label(
            container,
            text="وضعیت بازیکن",
            bg=BG,
            fg=WHITE,
            font=("Tahoma", 15, "bold")
        ).pack(anchor="e", pady=(35, 12))

        progress = ttk.Progressbar(
            container,
            style="Quest.Horizontal.TProgressbar",
            maximum=100,
            value=min(self.data["xp"], 100)
        )
        progress.pack(fill="x", pady=5)

        tk.Label(
            container,
            text=f"تجربه: {self.data['xp']} از ۱۰۰",
            bg=BG,
            fg=MUTED,
            font=("Tahoma", 10)
        ).pack(anchor="e")

        tk.Button(
            container,
            text="🚀 مشاهده مأموریت‌ها",
            command=lambda: self.navigate("مأموریت‌ها"),
            bg=ACCENT,
            fg=BG,
            activebackground=GOLD,
            font=("Tahoma", 12, "bold"),
            relief="flat",
            padx=25,
            pady=12,
            cursor="hand2"
        ).pack(anchor="e", pady=30)

    # ------------------------------------------
    # جابه‌جایی بین صفحات
    # ------------------------------------------

    
    def navigate(self, page):
        if page == "خانه":
            self.show_dashboard()

        elif page == "مأموریت‌ها":
            self.show_missions()

        elif page == "فروشگاه":
            self.show_shop()

        elif page == "کوله‌پشتی":
            self.show_inventory()

        elif page == "دستاوردها":
            self.show_achievements()

        elif page == "پروفایل":
            self.show_profile()

        elif page == "رتبه‌بندی":
            self.show_leaderboard()

        elif page == "تنظیمات":
            self.clear_content()
            self.page_title.config(text="تنظیمات")

            tk.Label(
                self.content,
                text="⚙️ تنظیمات",
                bg=BG,
                fg=ACCENT,
                font=("Tahoma", 22, "bold")
            ).pack(pady=80)

            tk.Label(
                self.content,
                text=f"بخش {page}",
                bg=BG,
                fg=ACCENT,
                font=("Tahoma", 23, "bold")
            ).pack(pady=80)

            tk.Label(
                self.content,
                text="این بخش در قسمت‌های بعدی تکمیل می‌شود.",
                bg=BG,
                fg=MUTED,
                font=("Tahoma", 12)
            ).pack()

    # ==========================================
    # سیستم مأموریت‌ها
    # ==========================================

    def create_missions(self):
        templates = [
            {
                "title": "رمزگشایی مقدماتی",
                "question": "کدام گزینه یک رمز عبور قوی‌تر است؟",
                "options": [
                    "123456",
                    "password",
                    "H@fez_92!Qx",
                    "abcdef"
                ],
                "answer": 2,
                "hint": "ترکیب حروف، اعداد و نشانه‌ها بهتر است."
            },
            {
                "title": "دانش رایانه",
                "question": "مغز اصلی رایانه کدام قطعه است؟",
                "options": [
                    "پردازنده",
                    "مانیتور",
                    "ماوس",
                    "بلندگو"
                ],
                "answer": 0,
                "hint": "این قطعه دستورها را پردازش می‌کند."
            },
            {
                "title": "دنیای اینترنت",
                "question": "HTTPS بیشتر برای چه چیزی استفاده می‌شود؟",
                "options": [
                    "افزایش صدای رایانه",
                    "ارتباط امن با وب‌سایت",
                    "خاموش کردن رایانه",
                    "ویرایش عکس"
                ],
                "answer": 1,
                "hint": "حرف S به امنیت اشاره دارد."
            },
            {
                "title": "هوش مصنوعی",
                "question": "کدام مورد نمونه‌ای از هوش مصنوعی است؟",
                "options": [
                    "ماشین‌حساب ساده",
                    "سیستم تشخیص گفتار",
                    "کابل برق",
                    "صفحه‌کلید"
                ],
                "answer": 1,
                "hint": "این فناوری می‌تواند گفتار انسان را تحلیل کند."
            },
            {
                "title": "برنامه‌نویسی",
                "question": "پسوند معمول فایل پایتون چیست؟",
                "options": [
                    ".txt",
                    ".jpg",
                    ".py",
                    ".mp3"
                ],
                "answer": 2,
                "hint": "نام این زبان Python است."
            },
            {
                "title": "امنیت دیجیتال",
                "question": "اگر یک ایمیل ناشناس لینک مشکوکی فرستاد، چه کار کنیم؟",
                "options": [
                    "فوراً روی لینک کلیک کنیم",
                    "اطلاعات شخصی وارد کنیم",
                    "بدون بررسی آن را باز نکنیم",
                    "آن را برای همه بفرستیم"
                ],
                "answer": 2,
                "hint": "اول باید فرستنده و آدرس لینک بررسی شود."
            },
            {
                "title": "شبکه‌های رایانه‌ای",
                "question": "Wi-Fi برای چه کاری استفاده می‌شود؟",
                "options": [
                    "اتصال بی‌سیم به شبکه",
                    "چاپ سه‌بعدی",
                    "افزایش حافظه",
                    "شارژ باتری"
                ],
                "answer": 0,
                "hint": "این فناوری بدون کابل ارتباط برقرار می‌کند."
            },
            {
                "title": "سخت‌افزار",
                "question": "RAM چه نوع حافظه‌ای است؟",
                "options": [
                    "حافظه موقت",
                    "حافظه دائمی",
                    "حافظه نوری",
                    "حافظه صوتی"
                ],
                "answer": 0,
                "hint": "با خاموش شدن دستگاه، اطلاعات موقت آن معمولاً پاک می‌شود."
            },
            {
                "title": "پایگاه داده",
                "question": "SQL بیشتر برای چه کاری استفاده می‌شود؟",
                "options": [
                    "مدیریت پایگاه داده",
                    "طراحی لباس",
                    "ساخت موسیقی",
                    "ویرایش ویدئو"
                ],
                "answer": 0,
                "hint": "این زبان با داده‌ها و جدول‌ها سروکار دارد."
            },
            {
                "title": "دانش دیجیتال",
                "question": "کدام گزینه یک سیستم‌عامل است؟",
                "options": [
                    "Windows",
                    "HTML",
                    "Python",
                    "JPEG"
                ],
                "answer": 0,
                "hint": "این سیستم‌عامل روی بسیاری از رایانه‌ها نصب است."
            }
        ]

        missions = []

        for number in range(1, 181):
            template = templates[(number - 1) % len(templates)]

            missions.append({
                "id": number,
                "title": f"{template['title']} شماره {number}",
                "question": template["question"],
                "options": template["options"].copy(),
                "answer": template["answer"],
                "hint": template["hint"],
                "reward": 10 + (number % 5) * 5,
                "xp": 20 + (number % 4) * 10
            })

        return missions

    # ==========================================
    # نمایش مأموریت‌ها
    # ==========================================



    def show_missions(self):
        self.root.unbind_all("<MouseWheel>")
        self.clear_content()
        self.page_title.config(text="مأموریت‌های سایبری")

        missions = self.create_missions()

        wrapper = tk.Frame(
            self.content,
            bg=BG,
            padx=25,
            pady=15
        )
        wrapper.pack(fill="both", expand=True)

        tk.Label(
            wrapper,
            text="🎯 مرکز مأموریت‌ها",
            bg=BG,
            fg=ACCENT,
            font=("Tahoma", 21, "bold")
        ).pack(anchor="e", pady=10)

        completed = len(self.data["completed"])

        tk.Label(
            wrapper,
            text=f"تکمیل‌شده: {completed} از ۱۸۰",
            bg=BG,
            fg=GOLD,
            font=("Tahoma", 11)
        ).pack(anchor="e", pady=5)

        progress = ttk.Progressbar(
            wrapper,
            maximum=180,
            value=min(completed, 180),
            style="Quest.Horizontal.TProgressbar"
        )
        progress.pack(fill="x", pady=10)

        list_container = tk.Frame(wrapper, bg=BG)
        list_container.pack(fill="both", expand=True)

        canvas = tk.Canvas(
            list_container,
            bg=BG,
            highlightthickness=0
        )

        scrollbar = ttk.Scrollbar(
            list_container,
            orient="vertical",
            command=canvas.yview
        )

        mission_frame = tk.Frame(canvas, bg=BG)

        window_id = canvas.create_window(
            (0, 0),
            window=mission_frame,
            anchor="nw"
        )

        mission_frame.bind(
            "<Configure>",
            lambda event: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.bind(
            "<Configure>",
            lambda event: canvas.itemconfigure(
                window_id,
                width=event.width
            )
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def scroll_missions(event):
            canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

        canvas.bind_all(
            "<MouseWheel>",
            scroll_missions
        )

        for mission in missions:
            mission_id = mission["id"]
            is_completed = mission_id in self.data["completed"]

            card = tk.Frame(
                mission_frame,
                bg=PANEL,
                padx=15,
                pady=13
            )
            card.pack(fill="x", pady=5, padx=5)

            status = "✓ انجام‌شده" if is_completed else "● آماده"

            tk.Label(
                card,
                text=f"{mission['title']} | {status}",
                bg=PANEL,
                fg=GREEN if is_completed else WHITE,
                font=("Tahoma", 11, "bold"),
                anchor="e"
            ).pack(fill="x")

            tk.Label(
                card,
                text=f"جایزه: {mission['reward']} سکه | تجربه: {mission['xp']} XP",
                bg=PANEL,
                fg=GOLD,
                font=("Tahoma", 9),
                anchor="e"
            ).pack(fill="x", pady=5)

            tk.Button(
                card,
                text="مشاهده مأموریت",
                command=lambda m=mission: self.start_mission(m),
                bg=PANEL_LIGHT,
                fg=ACCENT,
                activebackground=ACCENT,
                activeforeground=BG,
                relief="flat",
                font=("Tahoma", 9, "bold"),
                cursor="hand2"
            ).pack(anchor="e")


    # ==========================================
    # بررسی پاسخ
    # ==========================================
    def start_mission(self, mission):
        self.current_mission = mission
        self.selected_answer = tk.IntVar(value=-1)

        self.clear_content()
        self.page_title.config(text="انجام مأموریت")

        container = tk.Frame(
            self.content,
            bg=BG,
            padx=35,
            pady=25
        )
        container.pack(fill="both", expand=True)

        tk.Label(
            container,
            text=f"🎯 {mission['title']}",
            bg=BG,
            fg=ACCENT,
            font=("Tahoma", 21, "bold")
        ).pack(anchor="e", pady=20)

        tk.Label(
            container,
            text=mission["question"],
            bg=BG,
            fg=WHITE,
            font=("Tahoma", 15, "bold"),
            wraplength=850
        ).pack(anchor="e", pady=25)

        for index, option in enumerate(mission["options"]):
            tk.Radiobutton(
                container,
                text=option,
                variable=self.selected_answer,
                value=index,
                bg=BG,
                fg=WHITE,
                selectcolor=PANEL,
                activebackground=BG,
                activeforeground=ACCENT,
                font=("Tahoma", 12),
                anchor="e",
                justify="right"
            ).pack(anchor="e", pady=9)

        tk.Button(
            container,
            text="💡 نمایش راهنما",
            command=self.show_hint,
            bg=PANEL_LIGHT,
            fg=GOLD,
            font=("Tahoma", 10, "bold"),
            relief="flat",
            padx=20,
            pady=9
        ).pack(anchor="e", pady=15)

        tk.Button(
            container,
            text="✅ ثبت پاسخ",
            command=self.check_answer,
            bg=ACCENT,
            fg=BG,
            font=("Tahoma", 12, "bold"),
            relief="flat",
            padx=25,
            pady=12
        ).pack(anchor="e", pady=10)

        tk.Button(
            container,
            text="⬅ بازگشت به مأموریت‌ها",
            command=self.show_missions,
            bg=PANEL_LIGHT,
            fg=WHITE,
            font=("Tahoma", 10),
            relief="flat",
            padx=20,
            pady=9
        ).pack(anchor="e")

    def check_answer(self):
        mission = self.current_mission
        selected = self.selected_answer.get()

        if selected == -1:
            messagebox.showwarning(
                "انتخاب پاسخ",
                "لطفاً ابتدا یک گزینه را انتخاب کن."
            )
            return

        if mission["id"] in self.data["completed"]:
            messagebox.showinfo(
                "مأموریت تکراری",
                "این مأموریت قبلاً انجام شده است."
            )
            return

        if selected == mission["answer"]:
            self.data["completed"].append(mission["id"])

            self.add_xp(mission["xp"])
            self.data["coins"] += mission["reward"]

            self.save_data()

            messagebox.showinfo(
                "موفقیت!",
                f"آفرین! پاسخ درست بود.\n"
                f"{mission['reward']} سکه و "
                f"{mission['xp']} امتیاز تجربه گرفتی."
            )

        else:
            messagebox.showerror(
                "پاسخ اشتباه",
                "این پاسخ درست نیست. دوباره تلاش کن!"
            )
            return

        self.show_missions()

    # ==========================================
    # سیستم راهنمایی
    # ==========================================

    def show_hint(self):
        messagebox.showinfo(
            "راهنمای مأموریت",
            self.current_mission["hint"]
        )

    # ==========================================
    # امتیاز تجربه و ارتقای سطح
    # ==========================================

    def add_xp(self, amount):
        self.data["xp"] += amount

        while self.data["xp"] >= self.xp_for_next_level():
            required = self.xp_for_next_level()
            self.data["xp"] -= required
            self.data["level"] += 1

            messagebox.showinfo(
                "ارتقای سطح!",
                f"تبریک! به سطح {self.data['level']} رسیدی!"
            )

        self.save_data()

    def xp_for_next_level(self):
        return 100 + (self.data["level"] - 1) * 50

    # ==========================================
    # فروشگاه سایبری
    # ==========================================

    def create_shop_items(self):
        return [
            {
                "id": "theme_blue",
                "name": "تم آبی نئونی",
                "description": "ظاهر آبی مخصوص هکرهای حرفه‌ای",
                "price": 100,
                "type": "theme"
            },
            {
                "id": "theme_gold",
                "name": "تم طلایی",
                "description": "ظاهر طلایی ویژه",
                "price": 250,
                "type": "theme"
            },
            {
                "id": "title_pro",
                "name": "عنوان حرفه‌ای",
                "description": "عنوان ویژه برای پروفایل",
                "price": 150,
                "type": "title"
            },
            {
                "id": "xp_100",
                "name": "بسته تجربه",
                "description": "دریافت ۱۰۰ امتیاز تجربه",
                "price": 120,
                "type": "xp"
            },
            {
                "id": "xp_500",
                "name": "بسته تجربه بزرگ",
                "description": "دریافت ۵۰۰ امتیاز تجربه",
                "price": 450,
                "type": "xp"
            },
            {
                "id": "coin_100",
                "name": "کیسه سکه",
                "description": "دریافت ۱۰۰ سکه جایزه",
                "price": 0,
                "type": "coins"
            },
            {
                "id": "badge_star",
                "name": "نشان ستاره",
                "description": "نشان مخصوص پروفایل",
                "price": 300,
                "type": "badge"
            },
            {
                "id": "badge_cyber",
                "name": "نشان سایبری",
                "description": "نشان مخصوص بازیکنان سایبری",
                "price": 500,
                "type": "badge"
            }
        ]

    # ==========================================
    # صفحه فروشگاه
    # ==========================================

    def show_shop(self):
        self.clear_content()
        self.current_page = "فروشگاه"
        self.page_title.config(text="فروشگاه")

        container = tk.Frame(
            self.content,
            bg=BG,
            padx=25,
            pady=20
        )
        container.pack(fill="both", expand=True)

        tk.Label(
            container,
            text="🛒 فروشگاه سایبری",
            bg=BG,
            fg=ACCENT,
            font=("Tahoma", 22, "bold")
        ).pack(anchor="e")

        tk.Label(
            container,
            text=f"موجودی کیف پول: {self.data['coins']} سکه",
            bg=BG,
            fg=GOLD,
            font=("Tahoma", 12, "bold")
        ).pack(anchor="e", pady=12)

        canvas = tk.Canvas(
            container,
            bg=BG,
            highlightthickness=0
        )

        scrollbar = ttk.Scrollbar(
            container,
            orient="vertical",
            command=canvas.yview
        )

        items_frame = tk.Frame(
            canvas,
            bg=BG
        )

        items_frame.bind(
            "<Configure>",
            lambda event: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        window_id = canvas.create_window(
            (0, 0),
            window=items_frame,
            anchor="nw"
        )

        def resize_items(event):
            canvas.itemconfigure(
                window_id,
                width=event.width
            )

        canvas.bind("<Configure>", resize_items)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        for item in self.create_shop_items():
            card = tk.Frame(
                items_frame,
                bg=PANEL,
                padx=18,
                pady=15
            )
            card.pack(
                fill="x",
                pady=6,
                padx=5
            )

            owned = item["id"] in self.data["inventory"]

            tk.Label(
                card,
                text=item["name"],
                bg=PANEL,
                fg=ACCENT,
                font=("Tahoma", 12, "bold")
            ).pack(anchor="e")

            tk.Label(
                card,
                text=item["description"],
                bg=PANEL,
                fg=MUTED,
                font=("Tahoma", 9)
            ).pack(anchor="e", pady=5)

            tk.Label(
                card,
                text=f"قیمت: {item['price']} سکه",
                bg=PANEL,
                fg=GOLD,
                font=("Tahoma", 10)
            ).pack(anchor="e")

            if owned:
                text = "✓ خریداری شده"
                command = lambda: None
                color = "#26364B"
            else:
                text = "خرید محصول"
                command = lambda i=item: self.buy_item(i)
                color = PANEL_LIGHT

            tk.Button(
                card,
                text=text,
                command=command,
                bg=color,
                fg=WHITE,
                activebackground=ACCENT,
                relief="flat",
                font=("Tahoma", 10, "bold"),
                padx=18,
                pady=7
            ).pack(anchor="e", pady=(8, 0))

    # ==========================================
    # خرید محصول
    # ==========================================

    def buy_item(self, item):
        item_id = item["id"]

        if item_id in self.data["inventory"]:
            messagebox.showinfo(
                "فروشگاه",
                "این محصول را قبلاً خریداری کرده‌ای."
            )
            return

        price = item["price"]

        if self.data["coins"] < price:
            messagebox.showwarning(
                "سکه کافی نیست",
                "برای خرید این محصول سکه بیشتری لازم داری."
            )
            return

        confirm = messagebox.askyesno(
            "تأیید خرید",
            f"آیا می‌خواهی «{item['name']}» را بخری؟"
        )

        if not confirm:
            return

        self.data["coins"] -= price
        self.data["inventory"].append(item_id)

        self.apply_shop_item(item)

        self.save_data()

        messagebox.showinfo(
            "خرید موفق",
            f"محصول «{item['name']}» خریداری شد!"
        )

        self.show_shop()

    # ==========================================
    # اعمال محصول خریداری‌شده
    # ==========================================

    def apply_shop_item(self, item):
        if item["id"] == "xp_100":
            self.add_xp(100)

        elif item["id"] == "xp_500":
            self.add_xp(500)

        elif item["id"] == "coin_100":
            self.data["coins"] += 100

        elif item["type"] == "theme":
            self.data["active_theme"] = item["id"]

        elif item["type"] == "title":
            self.data["active_title"] = item["id"]

        elif item["type"] == "badge":
            self.data["active_badge"] = item["id"]

    # ==========================================
    # کیف پول
    # ==========================================

    def show_wallet(self):
        self.clear_content()
        self.current_page = "کیف پول"
        self.page_title.config(text="کیف پول")

        container = tk.Frame(
            self.content,
            bg=BG,
            padx=35,
            pady=30
        )
        container.pack(fill="both", expand=True)

        tk.Label(
            container,
            text="🪙 کیف پول سایبری",
            bg=BG,
            fg=GOLD,
            font=("Tahoma", 23, "bold")
        ).pack(anchor="e", pady=15)

        tk.Label(
            container,
            text=str(self.data["coins"]),
            bg=BG,
            fg=GOLD,
            font=("Tahoma", 38, "bold")
        ).pack(anchor="e", pady=10)

        tk.Label(
            container,
            text="موجودی فعلی به سکه",
            bg=BG,
            fg=MUTED,
            font=("Tahoma", 11)
        ).pack(anchor="e")

        tk.Button(
            container,
            text="🎁 دریافت جایزه روزانه",
            command=self.daily_reward,
            bg=ACCENT,
            fg=BG,
            font=("Tahoma", 11, "bold"),
            relief="flat",
            padx=20,
            pady=10
        ).pack(anchor="e", pady=30)

        tk.Button(
            container,
            text="بازگشت به فروشگاه",
            command=self.show_shop,
            bg=PANEL_LIGHT,
            fg=WHITE,
            font=("Tahoma", 10),
            relief="flat",
            padx=20,
            pady=9
        ).pack(anchor="e")

    # ==========================================
    # جایزه روزانه
    # ==========================================

    def daily_reward(self):
        today = datetime.now().strftime("%Y-%m-%d")

        if self.data.get("last_daily_reward") == today:
            messagebox.showinfo(
                "جایزه روزانه",
                "امروز جایزه‌ات را دریافت کرده‌ای!"
            )
            return

        reward = random.randint(25, 75)

        self.data["coins"] += reward
        self.data["last_daily_reward"] = today

        self.save_data()

        messagebox.showinfo(
            "جایزه دریافت شد!",
            f"تبریک! {reward} سکه دریافت کردی."
        )

        self.show_wallet()

    # ==========================================
    # صفحه کوله‌پشتی
    # ==========================================

    def show_inventory(self):
        self.clear_content()
        self.current_page = "کوله‌پشتی"
        self.page_title.config(text="کوله‌پشتی")

        container = tk.Frame(
            self.content,
            bg=BG,
            padx=30,
            pady=25
        )
        container.pack(fill="both", expand=True)

        tk.Label(
            container,
            text="🎒 کوله‌پشتی بازیکن",
            bg=BG,
            fg=ACCENT,
            font=("Tahoma", 22, "bold")
        ).pack(anchor="e", pady=15)

        inventory = self.data["inventory"]

        if not inventory:
            tk.Label(
                container,
                text="کوله‌پشتی خالی است!",
                bg=BG,
                fg=MUTED,
                font=("Tahoma", 13)
            ).pack(anchor="e", pady=20)

        else:
            names = {
                "theme_blue": "تم آبی نئونی",
                "theme_gold": "تم طلایی",
                "title_pro": "عنوان حرفه‌ای",
                "xp_100": "بسته تجربه ۱۰۰",
                "xp_500": "بسته تجربه ۵۰۰",
                "coin_100": "کیسه سکه",
                "badge_star": "نشان ستاره",
                "badge_cyber": "نشان سایبری"
            }

            for item_id in inventory:
                tk.Label(
                    container,
                    text="✓  " + names.get(item_id, item_id),
                    bg=PANEL,
                    fg=WHITE,
                    font=("Tahoma", 11),
                    padx=15,
                    pady=12
                ).pack(fill="x", pady=4)

    # ==========================================
    # پاداش دادن به بازیکن
    # ==========================================

    def add_coins(self, amount):
        self.data["coins"] += amount
        self.save_data()

    def spend_coins(self, amount):
        if self.data["coins"] < amount:
            return False

        self.data["coins"] -= amount
        self.save_data()
        return True

    # ==========================================
    # تنظیمات حرفه‌ای
    # ==========================================

    def show_settings(self):
        self.clear_content()
        self.current_page = "تنظیمات"
        self.page_title.config(text="تنظیمات")

        container = tk.Frame(
            self.content,
            bg=BG,
            padx=35,
            pady=25
        )
        container.pack(fill="both", expand=True)

        tk.Label(
            container,
            text="⚙️ مرکز تنظیمات",
            bg=BG,
            fg=ACCENT,
            font=("Tahoma", 22, "bold")
        ).pack(anchor="e", pady=15)

        sound_var = tk.BooleanVar(
            value=self.data["settings"].get("sound", True)
        )

        notify_var = tk.BooleanVar(
            value=self.data["settings"].get("notifications", True)
        )

        tk.Checkbutton(
            container,
            text="فعال بودن صداها",
            variable=sound_var,
            command=lambda: self.update_setting(
                "sound", sound_var.get()
            ),
            bg=BG,
            fg=WHITE,
            selectcolor=PANEL,
            activebackground=BG,
            font=("Tahoma", 11)
        ).pack(anchor="e", pady=10)

        tk.Checkbutton(
            container,
            text="فعال بودن اعلان‌ها",
            variable=notify_var,
            command=lambda: self.update_setting(
                "notifications", notify_var.get()
            ),
            bg=BG,
            fg=WHITE,
            selectcolor=PANEL,
            activebackground=BG,
            font=("Tahoma", 11)
        ).pack(anchor="e", pady=10)

        tk.Frame(
            container,
            bg=PANEL_LIGHT,
            height=2
        ).pack(fill="x", pady=20)

        tk.Button(
            container,
            text="💾 ذخیره تنظیمات",
            command=self.save_data,
            bg=ACCENT,
            fg=BG,
            font=("Tahoma", 11, "bold"),
            relief="flat",
            padx=20,
            pady=10
        ).pack(anchor="e", pady=8)

        tk.Button(
            container,
            text="📦 ساخت نسخه پشتیبان",
            command=self.create_backup,
            bg=PANEL_LIGHT,
            fg=WHITE,
            font=("Tahoma", 11),
            relief="flat",
            padx=20,
            pady=10
        ).pack(anchor="e", pady=8)

        tk.Button(
            container,
            text="📂 بازیابی نسخه پشتیبان",
            command=self.restore_backup,
            bg=PANEL_LIGHT,
            fg=WHITE,
            font=("Tahoma", 11),
            relief="flat",
            padx=20,
            pady=10
        ).pack(anchor="e", pady=8)

        tk.Button(
            container,
            text="📊 گزارش بازیکن",
            command=self.show_game_report,
            bg=PANEL_LIGHT,
            fg=WHITE,
            font=("Tahoma", 11),
            relief="flat",
            padx=20,
            pady=10
        ).pack(anchor="e", pady=8)

        tk.Button(
            container,
            text="⚠️ بازنشانی پیشرفت بازی",
            command=self.reset_progress,
            bg="#57232D",
            fg=WHITE,
            font=("Tahoma", 11, "bold"),
            relief="flat",
            padx=20,
            pady=10
        ).pack(anchor="e", pady=15)

    # ==========================================
    # تغییر تنظیمات
    # ==========================================

    def update_setting(self, key, value):
        self.data["settings"][key] = value
        self.save_data()

    # ==========================================
    # ساخت نسخه پشتیبان
    # ==========================================

    def create_backup(self):
        from tkinter import filedialog

        path = filedialog.asksaveasfilename(
            title="ذخیره نسخه پشتیبان",
            defaultextension=".json",
            filetypes=[
                ("JSON", "*.json")
            ],
            initialfile="Hafez_Backup.json"
        )

        if not path:
            return

        try:
            with open(path, "w", encoding="utf-8") as file:
                json.dump(
                    self.data,
                    file,
                    ensure_ascii=False,
                    indent=4
                )

            messagebox.showinfo(
                "پشتیبان‌گیری",
                "نسخه پشتیبان با موفقیت ساخته شد."
            )

        except Exception as error:
            messagebox.showerror(
                "خطا",
                str(error)
            )

    # ==========================================
    # بازیابی نسخه پشتیبان
    # ==========================================

    def restore_backup(self):
        from tkinter import filedialog

        path = filedialog.askopenfilename(
            title="انتخاب نسخه پشتیبان",
            filetypes=[
                ("JSON", "*.json")
            ]
        )

        if not path:
            return

        try:
            with open(path, "r", encoding="utf-8") as file:
                backup = json.load(file)

            if not isinstance(backup, dict):
                raise ValueError("ساختار فایل پشتیبان معتبر نیست.")

            required = [
                "username",
                "level",
                "xp",
                "coins",
                "completed",
                "inventory",
                "achievements"
            ]

            if not all(key in backup for key in required):
                raise ValueError("فایل پشتیبان ناقص است.")

            if not messagebox.askyesno(
                "تأیید بازیابی",
                "اطلاعات فعلی با نسخه پشتیبان جایگزین شود؟"
            ):
                return

            restored = DEFAULT_DATA.copy()
            restored.update(backup)

            restored["settings"] = {
                **DEFAULT_DATA["settings"],
                **backup.get("settings", {})
            }

            self.data = restored
            self.save_data()

            messagebox.showinfo(
                "بازیابی موفق",
                "اطلاعات بازی بازیابی شد."
            )

            self.show_dashboard()

        except Exception as error:
            messagebox.showerror(
                "خطای بازیابی",
                str(error)
            )

    # ==========================================
    # گزارش وضعیت بازی
    # ==========================================

    def show_game_report(self):
        completed = len(self.data["completed"])
        inventory = len(self.data["inventory"])
        achievements = len(self.data["achievements"])

        report = (
            "گزارش بازیکن\n"
            "----------------------\n"
            f"نام: {self.data['username']}\n"
            f"سطح: {self.data['level']}\n"
            f"تجربه: {self.data['xp']}\n"
            f"سکه: {self.data['coins']}\n"
            f"مأموریت تکمیل‌شده: {completed}\n"
            f"محصولات خریداری‌شده: {inventory}\n"
            f"دستاوردها: {achievements}\n"
            "----------------------"
        )

        messagebox.showinfo(
            "گزارش بازیکن",
            report
        )

    # ==========================================
    # بازنشانی پیشرفت
    # ==========================================

    def reset_progress(self):
        confirm = messagebox.askyesno(
            "بازنشانی بازی",
            "تمام پیشرفت‌های فعلی پاک می‌شوند.\n"
            "آیا مطمئنی؟"
        )

        if not confirm:
            return

        username = self.data["username"]

        self.data = DEFAULT_DATA.copy()
        self.data["settings"] = DEFAULT_DATA["settings"].copy()
        self.data["username"] = username

        self.save_data()

        messagebox.showinfo(
            "بازنشانی",
            "پیشرفت بازی بازنشانی شد."
        )

        self.show_dashboard()

def main():
    root = tk.Tk()
    app = HafezCyberQuest(root)
    root.mainloop()


if __name__ == "__main__":
    main()
