from flask import render_template, request
from . import view_bp
from models import db, Host, IPAddress, Group, HostGroup

def get_all_groups():
    return db.session.query(Group).all()

def get_ip_and_host_data(search_type=None, search_host=None, search_group=None):
    # Начинаем с базового запроса
    query = db.session.query(
        Host.zbxhost.label('host'),
        Host.type.label('type'),
        IPAddress.ip.label('ip'),
        Group.zbxgroup.label('group')
    ).outerjoin(IPAddress, IPAddress.hostid == Host.hostid) \
     .outerjoin(HostGroup, Host.hostid == HostGroup.hostid) \
     .outerjoin(Group, HostGroup.groupid == Group.groupid)
    
    # Фильтруем по типу, если он указан
    if search_type:
        query = query.filter(Host.type.ilike(f'%{search_type}%'))
    
    # Фильтруем по хосту, если он указан
    if search_host:
        query = query.filter(Host.zbxhost.ilike(f'%{search_host}%'))
    
    # Фильтруем по группе, если он указан
    if search_group:
        group_list = [group.strip() for group in search_group.split(',')]
        query = query.filter(Group.zbxgroup.in_(group_list))
    
    # Получаем все результаты
    results = query.all()
    return results

@view_bp.route('/')
def view():
    # Получаем параметры поиска из запроса
    search_host = request.args.get('search_host', '')
    search_type = request.args.get('search_type', '')
    search_group = request.args.get('search_group', '')
    
    # Передаем параметры в функцию для получения данных
    results = get_ip_and_host_data(search_type, search_host, search_group)
    groups = get_all_groups()
    # Возвращаем отрендеренный шаблон с результатами
    return render_template('view.html', results=results, groups=groups)
