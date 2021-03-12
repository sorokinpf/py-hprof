import hprof
import sys
h = hprof.open(sys.argv[1])
heap, = h.heaps

def dump_obj(obj):
    for field in obj.__dir__():
        if field=='<resolved_references>':
            continue
        value = obj.__getattr__(field)
        if '%s' % value.__class__ == 'hudson.util.Secret':
            value = value.value        
        print (f'{field}: {value}')

targets = list(heap.all_instances('hudson.util.Secret'))
for i in heap:
    obj = heap[i]
    fields = []
    try:
        fields = obj.__dir__()
    except:
        pass
    for field in fields:
        if obj.__getattr__(field) in targets:
            print (f'Found secret in object {obj} in {field} field')
            dump_obj(obj)