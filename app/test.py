temp = ["asdasd"]

def yo():
    val_1 = ["123"]
    val_2 = []
    if val_1:
        return ["1"]
    elif val_2:
        return ["2"]
    else:
        return None

val = yo()

if val is not None:
    print("We sendin'")
print(val)



# @router.get('/stream')
# async def sensor_data(request: Request):
#     async def sensor_data_generator():
#         prev_data = {"payload_name": "default", "payload_data": []}
#         global is_recording
#         prev_1 = {"payload_name": "default", "payload_data": []}
#         prev_2 = {"payload_name": "default", "payload_data": []}
#         data_1_success = False
#         data_2_success = False
#         counter_skip = 0
#         counter_sent = 0
#         start = time.time()
#         while True:

#             if await request.is_disconnected():
#                 break
#             try:
#                 data_1 = data_queue_1.get(block=False, timeout=0.01)
#                 prev_1 = data_1
#                 data_1_success = True
#             except queue.Empty:
#                 data_1 = prev_1
#                 data_1_success = False
#             try:
#                 data_2 = data_queue_2.get(block=False, timeout=0.01)
#                 prev_2 = data_2
#                 data_2_success = True
#             except queue.Empty:
#                 data_2 = prev_2
#                 data_2_success = False
#             data = _merge_payloads(data_1, data_2)
 
#             if is_recording and data['payload_name'] == "sensor_data":
#                 _save(data)
#             if data_1_success or data_2_success:
#                 yield {"event": "stream", "data": json.dumps(data)}
#                 counter_sent = counter_sent + 1
#             else:
#                 counter_skip = counter_skip + 1
            
#             # stop = time.time()
#             # print("LOOP (s): ", str(stop - start))
#             if (counter_skip % 50000 == 0):
#                 print("TIME________: ", str(time.time() - start))
#                 print("Times sent  : ", str(counter_sent))
#                 print("Times skips : ", str(counter_skip))
#                 counter_sent = 0
#                 counter_skip = 0
#                 start = time.time()
#             await asyncio.sleep(0.01)
            
#     return EventSourceResponse(sensor_data_generator())