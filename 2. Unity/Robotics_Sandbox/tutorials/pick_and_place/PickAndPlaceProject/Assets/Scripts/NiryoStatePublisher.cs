using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.NiryoMoveit;
using RosMessageTypes.Geometry;
using Unity.Robotics.ROSTCPConnector.ROSGeometry;
using Unity.Robotics.UrdfImporter;

public class NiryoStatePublisher : MonoBehaviour
{
    private const int k_NumRobotJoints = 6;

    // posts data to this communication channel ("/niryo_joints")
    [SerializeField] private string m_TopicName = "/niryo_joints";
    // root GameObject of the robot arm
    [SerializeField] private GameObject m_NiryoOne;
    // what the hand wants to pick up (the cube)
    [SerializeField] private GameObject m_Target;
    // what m_Target wants to be placed on (the table)
    [SerializeField] private GameObject m_TargetPlacement;
    // different from the standard rigidbody; links joints together in a specific parent-child chain, uses arrays to hold these joints
    [SerializeField] private ArticulationBody[] m_JointArticulationBodies;
    // holds the fixed downward rotation for picking up and placing objects cleanly.
    [SerializeField] private Quaternion m_PickOrientation;
    // opens a network port to Linux container; automatically converts Unity's 3D data to Linux's binary & vice versa
    private ROSConnection m_Ros;

    public ArticulationBody[] JointArticulationBodies => m_JointArticulationBodies;

    // Inside NiryoStatePublisher.cs:
    public static readonly string[] LinkNames = {
        "world/base_link/shoulder_link",
        "/arm_link",
        "/elbow_link",
        "/forearm_link",
        "/wrist_link",
        "/hand_link"
    };

    private void Start()
    {
        // automatically locates the ROS Connection component in scene
        m_Ros = ROSConnection.GetOrCreateInstance();
        m_Ros.RegisterPublisher<NiryoMoveitJointsMsg>(m_TopicName);

        m_PickOrientation = Quaternion.Euler(90f, 0f, 0f);
    }

    public void Publish()
    {
        var sourceDestinationMessage = new NiryoMoveitJointsMsg();

        sourceDestinationMessage.joints = new double[k_NumRobotJoints];

        for (var i = 0; i < k_NumRobotJoints; i++)
        {
            sourceDestinationMessage.joints[i] = m_JointArticulationBodies[i].jointPosition[0];
        }

        // pick pose
        sourceDestinationMessage.pick_pose = new PoseMsg
        {
            position = m_Target.transform.position.To<FLU>(),
            orientation = Quaternion.Euler(90, m_Target.transform.eulerAngles.y, 0).To<FLU>()
        };

        // place pose
        sourceDestinationMessage.place_pose = new PoseMsg()
        {
            position = m_TargetPlacement.transform.position.To<FLU>(),
            orientation = m_PickOrientation.To<FLU>()
        };

        m_Ros.Publish(m_TopicName, sourceDestinationMessage);
    }
}
