import smach
import rospy

class Released(smach.State):
    def __init__(self):
        super(Released, self).__init__(outcomes=['moving', 'error'])

    def execute(self, userdata):
        rospy.loginfo('Releasing payload...')
        time.sleep(1)
        if success_check():
            return 'moving'
        else:
            return 'error'

class Moving(smach.State):
    def __init__(self):
        super(Moving, self).__init__(outcomes=['paused', 'error'])

    def execute(self, userdata):
        rospy.loginfo('Moving...')
        time.sleep(5)
        if obstacle_detected():
            return 'paused'
        elif error_check():
            return 'error'
        else:
            # Assume reaching goal leads to finished
            return 'finished'

class Paused(smach.State):
    def __init__(self):
        super(Paused, self).__init__(outcomes=['resumed', 'cancelled'])

    def execute(self, userdata):
        rospy.loginfo('Pausing movement...')
        time.sleep(3)
        if obstacle_cleared_and_resume():
            return 'resumed'
        else:
            return 'cancelled'

sm = smach.StateMachine(outcomes=['finished', 'error'])

with sm:
    sm.add('RELEASED', Released(), transitions={'moving': 'MOVING', 'error': 'error'})
    sm.add('MOVING', Moving(), transitions={'paused': 'PAUSED', 'error': 'error'})
    sm.add('PAUSED', Paused(), transitions={'resumed': 'MOVING', 'cancelled': 'finished'})

if __name__ == '__main__':
    rospy.init_node('smach_task')
    sis = smach.IntrospectionStateMachine(sm)
    sis.execute()
