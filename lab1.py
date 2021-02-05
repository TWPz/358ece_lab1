#!/usr/bin/env python
# coding: utf-8

# #specs:
#     M/M/1 has infinite buffer while M/M/1/K has only size of K packets
#     
#     𝐹(𝑥) = 1 − 𝑒^(−𝜆)
#     𝒙 = − (𝟏/𝝀) 𝒍𝒏(𝟏 − 𝑼)
#     where U is a uniformly generated number and 𝑥 is the exponential random variable

# • λ = Average number of packets generated /arrived (packets per second)
# • L = Average length of a packet in bits.
# • α = Average number of observer events per second
# • C = The transmission rate of the output link in bits per second.
# • ρ = Utilization of the queue (= input rate/service rate = L λ/C)
# • E[N] = Average number of packets in the buffer/queue
# • PIDLE = The proportion of time the server is idle, i.e., no packets in the queue nor a packet is being transmitted.
# • PLOSS = The packet loss probability (for M/M/1/K queue). It is the ratio of the total number of packets lost due to
# buffer full condition to the total number of generated packets.

print("********** --- start of LAB 1 --- ***********")
# import necessary libraries
# introduce constants used in the lab
from random import seed
from random import random
import numpy as np
import math
import heapq

seed(358)
L = 2000
mil = C_rate = 1000000
#observer mulitple factor
lambda_alpha_factor = 5

#plot functions for Q3 and Q6
import matplotlib.pyplot as plt
# def plot_q3_4():
#     plt.title("E[N] - Rho ")
#     plt.plot(rho_list, EN, marker='.')
#     plt.xlabel('Rho values')
#     plt.ylabel('Average # of packets ')
#     plt.show()
#     plt.close()


#     plt.title("Pidle - Rho")
#     plt.xlabel('Rho values')
#     plt.ylabel('Percent of idle system')
#     plt.plot(rho_list, PIDLE, marker='.')
#     plt.show()
#     plt.close()


# def plot_q5_6(EN,PIDLE,PLOSS):
#         #set up lists to record data for each Packet size
#     EN_10 = []
#     EN_25 = []
#     EN_50 = []
#     EN_10 = EN[0:11]
#     EN_25 = EN[11:12+10]
#     EN_50 = EN[12+10:]
#     plt.title("E[N] - Rho ")
#     plt.plot(rho_list_second, EN_10,label="K = 10",marker='.')
#     plt.plot(rho_list_second, EN_25,label="K = 25",marker='.')
#     plt.plot(rho_list_second, EN_50,label="K = 50",marker='.')
#     plt.xlabel('Rho values')
#     plt.ylabel('Average # of packets ')
#     plt.grid()
#     plt.legend()
#     plt.show()
#     plt.close()
    
#     PIDLE_10 = []
#     PIDLE_25 = []
#     PIDLE_50 = []
#     PIDLE_10 = PIDLE[0:11]
#     PIDLE_25 = PIDLE[11:12+10]
#     PIDLE_50 = PIDLE[12+10:]
#     plt.title("Pidle - Rho")
#     plt.xlabel('Rho values')
#     plt.ylabel('Percent of idle system')
#     plt.plot(rho_list_second, PIDLE_10,label="K = 10",marker='.')
#     plt.plot(rho_list_second, PIDLE_25,label="K = 25",marker='.')
#     plt.plot(rho_list_second, PIDLE_50,label="K = 50",marker='.')
#     plt.grid()
#     plt.legend()
#     plt.show()
#     plt.close()

#     PLOSS_10 = []
#     PLOSS_25 = []
#     PLOSS_50 = []
#     PLOSS_10 = PLOSS[0:11]
#     PLOSS_25 = PLOSS[11:12+10]
#     PLOSS_50 = PLOSS[12+10:]
#     plt.title("Ploss - Rho")
#     plt.xlabel('Rho values')
#     plt.ylabel('Percent of loss system')
#     plt.plot(rho_list_second, PLOSS_10,label="K = 10",marker='.')
#     plt.plot(rho_list_second, PLOSS_25,label="K = 25",marker='.')
#     plt.plot(rho_list_second, PLOSS_50,label="K = 50",marker='.')
#     plt.grid()
#     plt.legend()
#     plt.show()
#     plt.close()

#Q1 1000 erv with lamba = 75
# get mean and variance of the 1000 rv

def exp_rad_var(lambda_value):
    return -1 * (math.log(1 - random())) / lambda_value

def mean_variance(data):
    mean = sum(data) / len(data)
    deviations = [(x - mean) ** 2 for x in data]
    variance = sum(deviations) / len(data)
    return mean,variance

def mean_variance_calculator(total_count, lambda_value):
    rad_list = [exp_rad_var(lambda_value) for _ in range(total_count)]
    expected_mean = 1/lambda_value
    expected_variance = expected_mean/lambda_value
    mean,variance = mean_variance(rad_list)
    return mean,variance,expected_mean,expected_variance


print("You Have Question Number Options as 1, 3, 6\n")
print("Question 1 contains answer for Q1")
print("Question 3 contains answer for Q2,Q3 and Q4")
print("Question 6 contains answer for Q5 and Q6\n")
while True:
    try:
        question_number = int(input("Enter a number for question now: "))
        break
    except:
        print("That's not a valid option!")

test_number = int(question_number)

if(test_number == 1):
    print("Question 1 with 6 runs on lambda = 75")

    for i in range(6):
        m,v,em,ev = mean_variance_calculator(1000,75)
        print("-----------------------  "+ str(i+1) +"  -----------------------")
        line_result = 'result mean: {:<20}      result variance: {:<20}'.format(m,v)
        line_expect = 'expect mean: {:<20}      expect variance: {:<20}'.format(em,ev)
        print(line_result)
        print(line_expect)
        print()

elif(test_number == 3):
        # ## Q2-3-4 M/M/1 Queue
    def infinite_buffer_event_list(Time,lambda_value,L=2000):
        #get observer rate from lambda_value (5 times as default)
        alpha = lambda_alpha_factor * lambda_value
        #initialization of time stream:
        departureStream = 0 
        arrivalStream = 0
        observerStream = 0
        
        #lists to hold times
        departureStream_list = []
        arrivalStream_list = []
        observerStream_list = []
        
        #get data packets running ...
        #start of simulation 
        while observerStream < Time: 
            # set up timestamps where observer checks the queue
            observerStream = exp_rad_var(alpha) + observerStream
            observerStream_list.append(observerStream) 
            
        while arrivalStream < Time:
            # set up arrival time and package size for each request throughout the queue
            arrivalStream = exp_rad_var(lambda_value) + arrivalStream
            packet_size = exp_rad_var(1/L)
            #observerStream = packet_size/C_rate
            service_time = packet_size/C_rate 
            
            arrivalStream_list.append(arrivalStream)
            # the first packet arrival T is d
            # If the queue is idle, then the departure time of packet 
            # will be its arrival time plus its transmission time (service time)
            # otherwise it would simply be departure time plus service time
            departureStream = arrivalStream + service_time if(arrivalStream > departureStream) else departureStream + service_time
            departureStream_list.append(departureStream)
        
        event_list = []
        for d in departureStream_list:
            event_list.append((d,"Departure"))
        for a in arrivalStream_list:
            event_list.append((a,"Arrival"))
        for o in observerStream_list:
            event_list.append((o,"Observer"))
            
        # put all the events in a list then sort them according to time
        event_list.sort(key=lambda tup: tup[0], reverse=False)
        return event_list,departureStream_list,arrivalStream_list,observerStream_list

    def infinite_buffer_calculation(data):
        arrival_count = 0 
        departure_count = 0 
        observer_count = 0 
        idle_c = 0
        avg_packet_list = []
        for key in data:
            if(key[1] == 'Arrival'):
                arrival_count = arrival_count + 1
            elif(key[1] == 'Departure'):
                departure_count = departure_count + 1
            elif(key[1] == 'Observer'):
                observer_count = observer_count + 1
                packets_in_buffer = arrival_count - departure_count
                if(packets_in_buffer == 0):
                    idle_c = idle_c + 1
                else:
                    avg_packet_list.append(packets_in_buffer)
                    
        p_idle = idle_c / observer_count
        avg_packet = sum(avg_packet_list)/len(avg_packet_list)
        return p_idle, avg_packet


    ##### with infinite buffer 
    ## due to the accuracy of the adding of decimals, we hardcode the sequence
    #https://stackoverflow.com/questions/588004/is-floating-point-math-broken
    rho_list = [0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95]

    def queue_with_infinite_buffer(Time,L=2000,C=C_rate):
        round_index = 0
        # two lists to hold the records of packets and IDLE ratio for each Rho value
        total_avg_packet = []
        total_p_idle = []
        # start processing
        for rho in rho_list:
            round_index = round_index + 1 
            # ---------- getting lambda value -----------
            lambda_value = rho / L * C
            print("PROCESS # ", round_index, "   rho: ", rho, "   lambda: ", lambda_value)
            # generate events list from DES generator 
            events,_,_,_ = infinite_buffer_event_list(Time,lambda_value,L)
            pidle,avg_packet = infinite_buffer_calculation(events)
            line_result = 'P idle:      {:<20}           E[N]:      {:<20}'.format(pidle,avg_packet)
            print(line_result)
            print()
            total_avg_packet.append(avg_packet)
            total_p_idle.append(pidle)
            
        return total_avg_packet,total_p_idle

    #running infinite buffer with T = 1000 s and giving relative plots
    print()
    print("Question 2-3 with T = 1000s but with no plots")
    EN,PIDLE = queue_with_infinite_buffer(1000)
    #plot_q3_4()

    print()
    print("Question 2-3 with T = 2000s but with no plots")
    #re-run with T = 2000s
    EN,PIDLE = queue_with_infinite_buffer(2000)
    #plot_q3_4()

    print()
    print("Question 4 with rho = 1.2 and T = 1000s")
    rho_list = [1.2]
    for i in range(6):
        EN,PIDLE = queue_with_infinite_buffer(1000)
    print("Question 4 with rho = 1.2 and T = 2000s")
    EN,PIDLE = queue_with_infinite_buffer(2000)
    EN,PIDLE = queue_with_infinite_buffer(2000)

elif(test_number == 6):
    def finite_buffer_event_list(Time,lambda_value,L=2000):
    #get observer rate from lambda_value (5 times as default)
        alpha = lambda_alpha_factor * lambda_value
        #initialization of time stream:
        
        #departureStream = 0 
        arrivalStream = 0
        observerStream = 0
        
        event_list = []
        #get data packets running ...
        #start of simulation 
        
        # set up timestamps where observer checks the queue  
        while observerStream < Time:
            observerStream = exp_rad_var(alpha) + observerStream
            event_list.append((observerStream,"Observer"))
            
        # set up arrival time and package size for each request throughout the queue
        while arrivalStream < Time:
            arrivalStream = exp_rad_var(lambda_value) + arrivalStream
            event_list.append((arrivalStream,"Arrival"))
            
        # put all the events in a list then sort them according to time
        event_list.sort(key=lambda tup: tup[0], reverse=False)
        return event_list

    def finite_buffer_calculation(event_list,K):
        arrival_count = 0 
        departure_count = 0
        observer_count = 0 
        
        idle_c = 0
        loss_c = 0
        
        avg_packet_list = []

        number_in_queue = 0
        #packet_count = 0
        packet_size = 0
        service_time = 0
        
        #calculations for generating departure stream 
        departureStream_list = []
        departureStream = 0 

        while len(event_list) > 0:
            # grab the first item(the smallest timestamp)
            event = heapq.heappop(event_list)
            if(event[1] == 'Arrival'):
                # packet_count = packet_count + 1 
                # if queue is not FULL, we update number of packets in the buffer
                # then fire a departure event based on arrival time
                if(number_in_queue < K): 
                    number_in_queue = number_in_queue + 1
                    arrival_count = arrival_count + 1           
                    service_time = (exp_rad_var(1/L))/C_rate
                    if(departureStream < event[0]):
                        departureStream = service_time + event[0]
                    else:
                        departureStream = departureStream + service_time
                    
                    # departure event added to list
                    event_list.append((departureStream,"Departure"))
                    
                # when queue is full, the packet is lost 
                else:
                    loss_c = loss_c + 1
    
            elif(event[1] == 'Departure'):
                #print("departure")
                departure_count = departure_count + 1
                number_in_queue = number_in_queue - 1
                
                
            elif(event[1] == 'Observer'):
                #print("observer")
                observer_count = observer_count + 1
                if(arrival_count - departure_count == 0):
                    idle_c = idle_c + 1
                else:
                    avg_packet_list.append(arrival_count - departure_count)
        
        p_idle = idle_c/observer_count
        p_loss = loss_c/(loss_c + arrival_count)
        #p_new_loss = loss_c / packet_count
        avg_packet = sum(avg_packet_list)/len(avg_packet_list)
        
        return p_idle, p_loss, avg_packet
        

    rho_list_second = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5]
    packet_list = [10, 25, 50]
    def queue_with_finite_buffer(Time,L=2000,C=C_rate):
        # start processing
        round_index = 0
        total_avg = []
        total_p_loss = []
        total_p_idle = []
        for K in packet_list:
            for rho in rho_list_second:
                round_index = round_index + 1 
                # ---------- getting lambda value
                lambda_value = rho / L * C
                print("PROCESS # ", round_index, "   rho: ", rho, "   lambda: ", lambda_value, "  K:", K)
                eve = finite_buffer_event_list(Time,lambda_value,L)
                pidle,ploss,e_n = finite_buffer_calculation(eve,K)
                line_result = 'P idle:      {:<30}      P loss:     {:<30}          E[N]: {:<30}'.format(pidle,ploss,e_n)
                print(line_result)
                print()
                total_p_idle.append(pidle)
                total_avg.append(e_n)
                total_p_loss.append(ploss)
            print("------------------------------------------------------------------------------------")
        return total_avg,total_p_idle,total_p_loss

    print()
    print("Question 5-6 with T = 1000s but with no plots")
    tv, tidle, tloss = queue_with_finite_buffer(1000)
    #plot_q5_6(tv,tidle,tloss)

    print()
    print("Question 5-6 with T = 2000s but with no plots")
    tv, tidle, tloss = queue_with_finite_buffer(2000)
else: print("Please Re-enter number to enter the program!")

print('\n' * 3)
print("********** --- end of LAB 1 --- ***********")