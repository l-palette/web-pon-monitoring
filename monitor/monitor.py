from flask import Flask, render_template, request, redirect, url_for
from . import monitor_bp
from database import db
from models import IPAddress, PonMonitoring, Host, Group, HostGroup
import pandas as pd
import matplotlib.pyplot as plt
import redis
import os

client = redis.StrictRedis(host='localhost', port=6379, db=0)

@monitor_bp.route('/')
def monitor():
    search_licence = request.args.get('search_licence', '')
    devices = get_ip_and_pon_monitoring_data(search_licence)
    return render_template('monitor.html', results=devices)

def get_ip_and_pon_monitoring_data(search_licence=None):
    query = db.session.query(
        Host.zbxhost.label('ip'),
        PonMonitoring.description.label('description'),
        PonMonitoring.interfacename.label('interfacename'),
        PonMonitoring.ponid.label('ponid')
    ).join(PonMonitoring, Host.hostid == PonMonitoring.hostid)
    
    if search_licence:
        query = query.filter(PonMonitoring.description.ilike(f'%{search_licence}%'))

    results = query.all()
    return results

def get_data_from_db(licence):
    """Получает данные из Redis для указанного лицевого счета"""
    try:
        client = redis.StrictRedis(host='localhost', port=6379, db=0)
        data = client.hgetall(licence)

        return [{'Time': k.decode('utf-8'), 'Value': float(v)} for k, v in data.items()]
    except Exception as e:
        print(f"Ошибка при получении данных из Redis: {e}")
        return []


@monitor_bp.route('/update', methods=['POST'])
def update():
    search_licence = request.form.get('search_licence', '')
    try:
        data = get_data_from_db(search_licence)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return redirect(url_for('monitor.monitor', search_licence=search_licence))

    if not data:
        print("No data found.")
        return redirect(url_for('monitor.monitor', search_licence=search_licence))

    df = pd.DataFrame(data)
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S')

    plt.figure(figsize=(10, 5))
    plt.plot(df['Time'], df['Value'], marker='o')
    plt.title('График значений по времени')
    plt.xlabel('Время')
    plt.ylabel('Значение')
    plt.grid()
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Сохраните график в статической папке
    plot_filename = f'plot_{search_licence}.png'
    plot_filepath = os.path.join('static', plot_filename)  # Путь к статической папке
    plt.savefig(plot_filepath)
    plt.close()

    # Перенаправьте на страницу dashboard с именем файла графика
    return redirect(url_for('monitor.dashboard', plot_filename=plot_filename))

@monitor_bp.route('/dashboard')
def dashboard():
    plot_filename = request.args.get('plot_filename', None)
    return render_template('dashboard.html', plot_filename=plot_filename)
