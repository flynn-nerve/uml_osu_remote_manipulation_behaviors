#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexible_manipulation_flexbe_states.setup_proxy_moveit_client_state import SetupProxyMoveItClientState
from flexbe_states.log_state import LogState
from flexible_manipulation_flexbe_states.get_joint_values_from_srdf_config_state import GetJointValuesFromSrdfConfigState
from flexible_manipulation_flexbe_states.joint_values_to_moveit_plan_state import JointValuesToMoveItPlanState
from flexible_manipulation_flexbe_states.execute_known_trajectory_state import ExecuteKnownTrajectoryState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Jul 29 2020
@author: Brian Flynn
'''
class demo_flexbe_manipulationSM(Behavior):
	'''
	Simple FlexBE manipulation behavior to demonstrate functionality of system
	'''


	def __init__(self):
		super(demo_flexbe_manipulationSM, self).__init__()
		self.name = 'demo_flexbe_manipulation'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:95 y:629, x:806 y:420
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.action_topic = "/move_group"
		_state_machine.userdata.trajectory_action_topic = "ur5e/arm_controller/follow_joint_trajectory"
		_state_machine.userdata.move_group = "manipulator"
		_state_machine.userdata.config_up = "up"
		_state_machine.userdata.config_default = "default"
		_state_machine.userdata.components = None

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:74 y:38
			OperatableStateMachine.add('InitializeMoveit',
										SetupProxyMoveItClientState(robot_description="/robot_description", robot_description_semantic=None, move_group_capabilities="/move_group", action_type_and_topics=[["MoveGroupAction",["/move_group"]]], enter_wait_duration=0.0),
										transitions={'connected': 'LoggerConnected', 'topics_unavailable': 'failed', 'param_error': 'failed'},
										autonomy={'connected': Autonomy.Off, 'topics_unavailable': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'robot_name': 'robot_name', 'move_groups': 'move_groups'})

			# x:255 y:130
			OperatableStateMachine.add('LoggerConnected',
										LogState(text="filler", severity=Logger.REPORT_HINT),
										transitions={'done': 'GetDefaultPosition'},
										autonomy={'done': Autonomy.Off})

			# x:73 y:222
			OperatableStateMachine.add('GetDefaultPosition',
										GetJointValuesFromSrdfConfigState(),
										transitions={'retrieved': 'PlanMovement', 'param_error': 'failed'},
										autonomy={'retrieved': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'robot_name': 'robot_name', 'selected_move_group': 'move_group', 'config_name': 'config_default', 'move_group': 'move_group', 'joint_names': 'joint_names', 'joint_values': 'joint_values'})

			# x:76 y:369
			OperatableStateMachine.add('PlanMovement',
										JointValuesToMoveItPlanState(timeout=5.0, enter_wait_duration=0.0, action_topic=None),
										transitions={'planned': 'ExecuteMovement', 'failed': 'failed', 'topics_unavailable': 'failed', 'param_error': 'failed'},
										autonomy={'planned': Autonomy.Off, 'failed': Autonomy.Off, 'topics_unavailable': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'action_topic': 'action_topic', 'move_group': 'move_group', 'joint_names': 'joint_names', 'joint_values': 'joint_values', 'joint_trajectory': 'joint_trajectory'})

			# x:76 y:472
			OperatableStateMachine.add('ExecuteMovement',
										ExecuteKnownTrajectoryState(timeout=3.0, max_delay=5.0, wait_duration=0.25, action_topic="/execute_trajectory"),
										transitions={'done': 'GetUpPosition', 'failed': 'failed', 'param_error': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'action_topic': 'action_topic', 'trajectory': 'joint_trajectory', 'status_text': 'status_text', 'goal_names': 'goal_names', 'goal_values': 'goal_values'})

			# x:494 y:131
			OperatableStateMachine.add('GetUpPosition',
										GetJointValuesFromSrdfConfigState(),
										transitions={'retrieved': 'PlanMovement2', 'param_error': 'failed'},
										autonomy={'retrieved': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'robot_name': 'robot_name', 'selected_move_group': 'move_group', 'config_name': 'config_up', 'move_group': 'move_group', 'joint_names': 'joint_names', 'joint_values': 'joint_values'})

			# x:906 y:225
			OperatableStateMachine.add('PlanMovement2',
										JointValuesToMoveItPlanState(timeout=5.0, enter_wait_duration=0.5, action_topic=None),
										transitions={'planned': 'ExecuteMovement2', 'failed': 'failed', 'topics_unavailable': 'failed', 'param_error': 'failed'},
										autonomy={'planned': Autonomy.Off, 'failed': Autonomy.Off, 'topics_unavailable': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'action_topic': 'action_topic', 'move_group': 'move_group', 'joint_names': 'joint_names', 'joint_values': 'joint_values', 'joint_trajectory': 'joint_trajectory'})

			# x:906 y:449
			OperatableStateMachine.add('ExecuteMovement2',
										ExecuteKnownTrajectoryState(timeout=3.0, max_delay=5.0, wait_duration=0.25, action_topic="/execute_trajectory"),
										transitions={'done': 'finished', 'failed': 'failed', 'param_error': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'action_topic': 'action_topic', 'trajectory': 'joint_trajectory', 'status_text': 'status_text', 'goal_names': 'goal_names', 'goal_values': 'goal_values'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
