# coding: utf-8
# -*- coding: utf-8 -*-
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, ConversationHandler) 
import telegram
from maxsulot import *
from function import *
import json
import ast
import datetime


Token='1573065998:AAEp502bdMmXOnBboaZ8_PZcTz81cN8VcY0'
bot=telegram.Bot(Token)
Uzbutton=ReplyKeyboardMarkup([
    ["✏️ Buyurtma berish"],
    ["⚙️ Bizning hizmatlar","📞 Biz bilan bog'lanish"]
], resize_keyboard=True)

global i, index, Zakzlar, add, S, Jami, User, Users, JamiNarx
Zakazlar=[]
add={'Nomi':'', 'Rangi':'', 'Kg':'', 'Narx':'', 'Dona':'', 'Karobka':'', 'Jami':''}
i=0
index=-1
S=''
Users=''
Jami=JamiNarx=0
User={'Fio':'', 'Tel':'', 'Username':''}
messageH, unMessage="","Aniqlanmagan so'rov, bot faqat maxsus buyruqlarga javob qaytara oladi"
def start(update, context):
    message="<b>Assalom alykum Life Tech sizni qutlaydi va hamkorlikka chorlaydi.</b> \n\n✒️ Life Tech kompaniyasi haqidagi har qanday ma'lumotlarni sizga yetqizaman. \n✒️ Sizni qiziqtirgan savol va takliflaringizni Life Tech adminlariga yuboraman."
    update.message.reply_photo( photo=open('boticon.png', 'rb'), caption=message,  reply_markup=Uzbutton, parse_mode='HTML')
    return 2
def inline_callback(update, context):
    global i, narx, index,S, Jami, User,Users, add, JamiNarx, Zakazlar
    query=update.callback_query
    fun=json.loads(query.data)

    if fun['fun']=='zakazQ':
        query.message.reply_photo(photo=open('boticon.png', 'rb'), caption='Online')
    # Zakaz maxsulot
    if fun['fun']=="ZakazM":
        index+=1
        print(User['Fio'])
        query.message.delete()
        Zakazlar.append(add)
        Kraskalar(query)
    if fun['fun']=='Rangi':
        query.message.delete()
        Zakazlar[index]['Nomi']=Kraska[int(fun['index'])]['Nomi']
        Ranglar(int(fun['index']), query)
    if fun['fun']=='Kg':
        query.message.delete()
        Zakazlar[index]['Rangi']=Rang[int(fun['rang'])]
        Kglar(int(fun['index']), query)
    if fun['fun']=='Narxi':
        query.message.delete()
        Zakazlar[index]['Kg']=str(Kg[int(fun['kg'])])+'kg'
        Narxlar(int(fun['index']), query)
    if fun['fun']=='Soni':
        query.message.delete()
        Zakazlar[index]['Narx']=str(Narx[int(fun['narx'])])+" so'm/dona"
        narx=Narx[int(fun['narx'])]
        Sonlar(int(fun['index']), query)
    if fun['fun']=='Count':
        query.message.delete()
        if fun['soni']=='🛢 Dona':
            query.message.reply_html('📍\n🛢 Ilsimos maxsulotning dona sonini kiriting\n<b>☝️ Masalan:</b> <i>(<b>Dona soni:</b>20)</i>\n<b>Dona soni:</b>')
            i=1
        if fun['soni']=='📦 Karobka':
            query.message.reply_html('📍\n📦 Iltimos maxsulotning qadoqlangan sonini kiriting\n<b>☝️ Masalan:</b> <i>(<b>Qutilar soni:</b>20)</i>\n<b>Qutilar soni:</b>')
            i=2
    if fun['fun']=='Junatish':
        query.message.delete()
        butH=[
            [InlineKeyboardButton("✅ Tasdiqlash", callback_data=json.dumps({'fun':'Tasdiqlash', 'Id':query.message.chat.id}))],
            [InlineKeyboardButton("❌ Rad etish", callback_data=json.dumps({'fun':'Rad', 'Id':query.message.chat.id}))]
        ]
        query.message.reply_html(Users+S+JamiNarx)
        bot.send_message(chat_id=918692178, text=Users+S+JamiNarx,  parse_mode='HTML', reply_markup=InlineKeyboardMarkup(butH))
        S=''
        index=-1
        JamiNarx=''
        Zakazlar=[]
    if fun['fun']=="Tasdiqlash":
        text="📌 |  ✅\nAssalom alaykum xurmatli mijoz sizning buyurtmangiz tasdiqlandi iltimos biroz kuting, <b>Mustang</b> kompaniyasi xodimlari qisqa vaqatlar ichida siz bilan bg'lanishadi."
        Message=query.message.text+"\n\n<b>✅ Tasdiqlangan</b>"
        query.message.delete()
        bot.send_message(chat_id=int(fun['Id']), text=text,  parse_mode='HTML')
        query.message.reply_html(Message)
    if fun['fun']=="TasdiqlashR":
        text="📌 |  ✅\nAssalom alaykum xurmatli mijoz sizning buyurtmangiz tasdiqlandi iltimos biroz kuting, <b>Mustang</b> kompaniyasi xodimlari qisqa vaqatlar ichida siz bilan bg'lanishadi."
        Message=query.message.caption+"\n\n<b>✅ Tasdiqlangan</b>"
        query.message.delete()
        bot.send_message(chat_id=int(fun['Id']), text=text,  parse_mode='HTML')
        x="img/"+fun['img']+".jpg"
        query.message.reply_photo(photo=open(x, 'rb'), caption=Message, parse_mode="HTML")
    if fun['fun']=="Rad":
        text="❌\nAssalom alaykum xurmatli mijoz sizning buyurtmangiz bazi sabablarga ko'ra tasdiqlanmadi, Bunday sabablar uchun  <b>Mustang</b> kompaniyasi sizdan uzur so'raydi."
        Message=query.message.text+"\n\n<b>❌ Rad etildi</b>"
        query.message.delete()
        bot.send_message(chat_id=int(fun['Id']), text=text,  parse_mode='HTML')
        query.message.reply_html(Message)
    if fun['fun']=="RadR":
        text="❌\nAssalom alaykum xurmatli mijoz sizning buyurtmangiz bazi sabablarga ko'ra tasdiqlanmadi, Bunday sabablar uchun  <b>Mustang</b> kompaniyasi sizdan uzur so'raydi."
        Message=query.message.caption+"\n\n<b>❌ Rad etildi</b>"
        query.message.delete()
        bot.send_message(chat_id=int(fun['Id']), text=text,  parse_mode='HTML')
        x="img/"+fun['img']+".jpg"
        query.message.reply_photo(photo=open(x, 'rb'), caption=Message, parse_mode="HTML")
    if fun['fun']=='Delete':
        query.message.delete()
        query.message.reply_html("📌 | ❌ \nSizning buyurtmangiz muvofaqiyatli o'chirildi.☝️ Istasangiz <b>Buyurtma berish</b> tugmasi orqali qayta buyurtma berishindiz mumkin.")
        i=0
    if fun['fun']=='Qaytarish':
        query.message.delete()
        S=''
        index=0
        JamiNarx=''
        Zakazlar=[]
        User['Fio']=''
        Zakazlar.append(add)
        query.message.reply_html("📌 | ♻️ \nSizning eski buyurtmangizni bekor qildingiz.<b>☝️ Yangi maxsulotni tanlashingiz mumkin.</b>")
        Kraskalar(query)
        i=0
    if fun['fun']=='YozmaZ':
        query.message.delete()
        S=''
        index=0
        JamiNarx=''
        Zakazlar=[]
        User['Fio']=''
        query.message.reply_html("📌 |  ✍️\nIltimos buyurtma berish jarayonida imlo xatolariga etibor bering va namunaga binonan yozishingizni so'raymiz.\n<b>Namuna:</b>\n<i>Mustang qizil 25kg\n\nAlisher Parpiyev\n+998998780787</i>")
        i=5
    if fun['fun']=='Rasim':
        query.message.delete()
        S=''
        index=0
        JamiNarx=''
        Zakazlar=[]
        User['Fio']=''
        query.message.reply_html("📌 |  ✍️\nIltimos buyurtma rasimini yuboring.")
        i=6
          
def ZakazlarFun(update, context):
    global i, narx, index,S, Jami, User,Users, add, JamiNarx, Zakazlar
    if i==6:
        global x
        file_id = update.message.photo[-1]
        newFile = bot.getFile(file_id)
        x = datetime.datetime.now()
        x=x.strftime("%d")+x.strftime("%b")+x.strftime("%y")+x.strftime("%H")+x.strftime("%M")+x.strftime("%S")
        a="img/"+x+".jpg"
        newFile.download(a)
        butH=[
            [InlineKeyboardButton("✅ Tasdiqlash", callback_data=json.dumps({'fun':'TasdiqlashR', 'Id':update.message.chat.id, 'img':x}))],
            [InlineKeyboardButton("❌ Rad etish", callback_data=json.dumps({'fun':'RadR', 'Id':update.message.chat.id, 'img':x}))]
        ]
        text="\n\n<b>Ismi: </b>"+str(update.message.chat.first_name)+"\n<b>Familya: </b>"+str(update.message.chat.last_name)+"\n<b>Username:</b> @"+str(update.message.chat.username)+"\n<b>Text:</b> "+str(update.message.caption)
        x=x+".jpg"
        bot.sendPhoto(chat_id=918692178, photo=open(a, 'rb'), caption=text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(butH))
        i=-1

    if i==5:
        butH=[
            [InlineKeyboardButton("✅ Tasdiqlash", callback_data=json.dumps({'fun':'Tasdiqlash', 'Id':update.message.chat.id}))],
            [InlineKeyboardButton("❌ Rad etish", callback_data=json.dumps({'fun':'Rad', 'Id':update.message.chat.id}))]
        ]
        text=update.message.text
        update.message.reply_html("📌 |  ✅\nSizning buyurtmangiz <b>Mustang</b> kompaniyasi xodimlariga yuborildi. Iltimos biroz kuting korxona xodimlari qisqa vaqtlar ichida siz bilan bog'lanishadi.")
        bot.send_message(chat_id=918692178, text=text,  parse_mode='HTML', reply_markup=InlineKeyboardMarkup(butH))
    if i==4:
        User['Tel']=update.message.text
        Tekshir(update)
        i=-1

    if i==3:
        User['Fio']=update.message.text
        update.message.reply_html("<b>Telefon raqam:</b>")
        i=4
    if i==2:
        Zakazlar[index]['Karobka']=update.message.text+" quti"
        Zakazlar[index]['Dona']=str(int(update.message.text)*6)+" bonka"
        Zakazlar[index]['Jami']=str(int(update.message.text)*int(narx)*6)+" so'm."
        Jami= Jami+int(update.message.text)*int(narx)*6
        if User['Fio']!='':
            Tekshir(update)
            i=-1
        else: 
            update.message.reply_html("<b>Iltimos O'zingiz haqingizdagi ma'lumotlarni to'ldiring!!!</b>" )
            update.message.reply_html("<b>Ism Familya:</b> \n<i>(Mazalan: Alisher Parpiev)</i>")           
            i=3  
         
    if i==1:
        Zakazlar[index]['Jami']=str(int(update.message.text)*int(narx))+"so'm."
        Jami=Jami+int(update.message.text)*int(narx)
        Zakazlar[index]['Dona']=update.message.text+' bonka'
        Zakazlar[index]['Karobka']=str(int(int(update.message.text)/6))+' Quti'
        if User['Fio']!='':
            Tekshir(update)
            i=-1
        else: 
            update.message.reply_html("<b>Iltimos O'zingiz haqingizdagi ma'lumotlarni to'ldiring!!!</b>" )
            update.message.reply_html("<b>Ism Familya:</b> \n<i>(Mazalan: Alisher Parpiev)</i>")           
            i=3  
    if i==0:
        update.message.reply_html("<b>📌 | ⁉️\nAniqlanmagan so'rov bot faqat maxsus so'rovlarga javob qaytara oladi.</b>")
    if i==-1:
        i=0
    

def Tekshir(update):
    global i, narx, index,S, Jami, User,Users, add, JamiNarx, Zakazlarss
    Users='📌\n<b>👤 Zakaz Beruvchi</b>\n\n<b>👨‍💻 FIO:</b> '+User['Fio']+"\n<b>📱 Telefon raqami:</b> "+User['Tel']+"\n\n<b>🧾 Buyurtmalar</b>"
    S=S+"\n\n<b>"+str(index+1)+"-Maxsulot</b>\n<b>📍 Nomi:</b>"+Zakazlar[index]['Nomi']+"\n<b>📍 Rangi:</b>"+Zakazlar[index]['Rangi']+"\n<b>📍 Kg:</b>"+Zakazlar[index]['Kg']+"\n<b>📍Soni:</b>"+Zakazlar[index]['Dona']+"\n<b>📍 Karobka soni:</b>"+Zakazlar[index]['Karobka']+"\n<b>📍Dona narxi:</b>"+Zakazlar[index]['Narx']+"\n<b>📍Jami narxi:</b>"+Zakazlar[index]['Jami']
    JamiNarx="\n\n<b>💰 Jami summa:</b>"+str(Jami)
    butH=[
            [InlineKeyboardButton("✅ Zakazni yuborish", callback_data=json.dumps({'fun':'Junatish'}))],
            [InlineKeyboardButton("➕ Zakaz qo'shish", callback_data=json.dumps({'fun':'ZakazM'}))],
            [InlineKeyboardButton("♻️ Qayta zakaz berish", callback_data=json.dumps({'fun':'Qaytarish'}))],
            [InlineKeyboardButton("❌ O'chirish", callback_data=json.dumps({'fun':'Delete'}))]
        ]
    update.message.reply_html(Users+S+JamiNarx, reply_markup=InlineKeyboardMarkup(butH))

def Buyurtma(update, contect):
    global i, narx, index,S, Jami, User,Users, add, JamiNarx, Zakazlar
    S=''
    JamiNarx=''
    Zakazlar=[]
    index=-1
    butH=[
            [InlineKeyboardButton("🗂 Avtomatik Buyurtma", callback_data=json.dumps({'fun':'ZakazM'}))],
            [InlineKeyboardButton("📝 Qo'lyozma buyurtma", callback_data=json.dumps({'fun':'YozmaZ'}))],
            [InlineKeyboardButton("📸 Rasim yuborish", callback_data=json.dumps({'fun':'Rasim'}))],
        ]
    update.message.reply_photo( photo=open('boticon.png', 'rb'), caption='Assalom alaykum xurmatli mijoz. Siz Mustang',  reply_markup=InlineKeyboardMarkup(butH))


def Boglanish(update, contect):
    global i
    text="<b>📌 | 📱 \nUchko'prik Lak Bo'yoq MCHJ</b> ishonch raqamlari siz uchun xizmatda.\n📞 <b>Admin:     </b>+998905086006\n📞 <b>Hisobchi: </b>+998911413344\n📞 <b>Texnolog: </b>+998911470778"
    update.message.reply_html( text)
    i=0

def Hizmatlar(update, contect):
    global i
    text="<b>📌 | 📊\nUchko'prik Lak Bo'yoq MCHJ</b> quyidagi xizmatlarni o'z ichiga oladi.\n\n<b>Bizning Xizmatlar:</b>\n\n✅ Yuqori sifatli <b>Lak Bo'yoq</b> maxsulotlari ishlab chiqarish.\n✅ Suvli bo'yoqlar ishlab chiqarish.\n🚚 O'zbekiston bo'ylab yetkazib berish xizmati."
    update.message.reply_html( text)
    i=0

def main():
    updater=Updater('1573065998:AAEp502bdMmXOnBboaZ8_PZcTz81cN8VcY0', use_context=True)
    dispatcher=updater.dispatcher
    dispatcher.add_handler(CallbackQueryHandler(inline_callback))
    conv_handler=ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
                1:[CallbackQueryHandler(inline_callback)],
                2:[
                    MessageHandler(Filters.regex('^('+"/start"+')$'), start),
                    MessageHandler(Filters.regex('^('+"✏️ Buyurtma berish"+')$'), Buyurtma),
                    MessageHandler(Filters.regex('^('+"📞 Biz bilan bog'lanish"+')$'), Boglanish),
                    MessageHandler(Filters.regex('^('+"⚙️ Bizning hizmatlar"+')$'), Hizmatlar),
                ]
                },
        fallbacks=[MessageHandler(Filters.all, ZakazlarFun)]
        )
    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle() 


main()