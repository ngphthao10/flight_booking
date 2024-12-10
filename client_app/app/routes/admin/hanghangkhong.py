from flask import Blueprint, render_template, current_app, flash, request
import requests

hanghangkhong = Blueprint('hanghangkhong', __name__)

@hanghangkhong.route('/hang-hang-khong', methods=['GET'])
def get_hang_hang_khong():
    try:
        # Lấy tất cả các tham số query từ request
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        ma_hhk = request.args.get('ma_hhk', '')
        ten_hhk = request.args.get('ten_hhk', '')
        ma_qg = request.args.get('ma_qg', '')
        sort_by = request.args.get('sort_by', 'MaHHK')
        order = request.args.get('order', 'asc')

        # Tạo dictionary chứa tất cả các tham số query
        query_params = {
            'page': page,
            'per_page': per_page,
            'ma_hhk': ma_hhk,
            'ten_hhk': ten_hhk,
            'ma_qg': ma_qg,
            'sort_by': sort_by,
            'order': order
        }

        # Loại bỏ các tham số trống để không gửi lên API
        query_params = {k: v for k, v in query_params.items() if v}
        
        # Gọi API với các tham số đã được lọc
        response = requests.get(
            f"{current_app.config['API_URL']}/api/hang-hang-khong",
            params=query_params
        )
        response.raise_for_status()
        data = response.json()

        if not data['status']:
            raise Exception(data['message'])

        return render_template(
            'admin/hanghangkhong/hanghangkhong.html',
            hang_hang_khong=data.get('data', []),
            pagination={
                'page': data['pagination']['page'],
                'pages': data['pagination']['pages'],
                'total': data['pagination']['total'],
                'per_page': data['pagination']['per_page']
            },
            # Truyền các giá trị filter hiện tại để hiển thị trên form
            filters={
                'ma_hhk': ma_hhk,
                'ten_hhk': ten_hhk,
                'ma_qg': ma_qg,
                'sort_by': sort_by,
                'order': order
            },
            api_url=current_app.config['API_URL']
        )

    except Exception as e:
        flash(str(e), 'danger')
        return render_template(
            'admin/hanghangkhong/hanghangkhong.html',
            hang_hang_khong=[],
            pagination={'page': 1, 'pages': 1, 'total': 0, 'per_page': 10},
            filters={  # Trả về filters rỗng trong trường hợp lỗi
                'ma_hhk': '',
                'ten_hhk': '',
                'ma_qg': '',
                'sort_by': 'MaHHK',
                'order': 'asc'
            },
            api_url=current_app.config['API_URL']
        )

        