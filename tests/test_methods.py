import time
import slash
import requests
import threading

from butler import Butler

class ButlerTest(Butler):
    def get_test_get(self):
        return 'test get'

    def post_test_post(self):
        return 'test post'
        
    def put_test_put(self):
        return 'test put'
        
    def delete_test_delete(self):
        return 'test delete'

@slash.fixture
def run_server():
    butler = ButlerTest()
    t = threading.Thread(target=butler.run, kwargs={'host': 'localhost', 'port': '8888'})
    t.daemon = True
    t.start()
    time.sleep(1)

    def stop_server():
        requests.get('http://localhost:8888/stop')
        time.sleep(1)

    slash.add_cleanup(stop_server)

@slash.parametrize('method', ['get', 'post', 'put', 'delete'])
def test_methods(run_server, method):
    base_url = 'http://localhost:8888'
    r = getattr(requests, method)('{}/test_{}'.format(base_url, method))
    assert r.content == 'test {}'.format(method)

if __name__ == '__main__':
    ButlerTest().run(host='localhost', port='8888')
