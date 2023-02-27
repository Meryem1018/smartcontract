// SPDX-License-Identifier: MIT

pragma solidity >=0.7.0 <0.9.0; //version of Solidity usable

//contract starts here
contract SecureMonitoring {
    //Variables
    address private supervisor; //the supervisor represents the higher authority
    address private operator; //the routine operator
    enum WSNstate {
        dormant,
        deployed_in_plug_and_play,
        estimate_recorded,
        invalid_estimate,
        deployed_fully
    }
    WSNstate public state; //state of the Wireless Sensor Network
    string public estimate; //tells whether estimate has been recorded /calculating yet or invalid
    int256 private stateEstimate; //the state estimate calculated
    int256 private estimate_value;
    bool public anomaly_detected;
    enum anomalyType {
        type1,
        type2,
        type3
    }
    anomalyType public anomaly_type;
    mapping(address => uint256) public times_visited; //returns the number of times an account viewed the estimate
    uint256 private times_visited_by;
    //Modifiers
    modifier OnlySupervisor() {
        //only supervisor can call
        require(msg.sender == supervisor);
        _;
    }
    modifier OnlyOperator() {
        //only operator can call
        require(msg.sender == operator);
        _;
    }
    //Error
    error invalid_Estimate(int256 estimate_value);

    //Events
    //Estimation Events
    event WSN_deployed_in_plug_and_play(address operator);
    event estimate_recorded(address operator);
    event invalid_estimate(address operator);
    event no_anomaly_is_detected(address operator);
    event anomaly_is_detected(address operator);

    //Anomaly events
    event type1anomaly_detected(address operator, int256 value);
    event type2anomaly_detected(address operator, int256 value);
    event type3anomaly_detected(address operator, int256 value);

    //Emergency Events
    event WSN_deployed_fully(address supervisor);
    event anomaly_confirmed(address supervisor);
    event alarm_raised(address supervisor);

    //Functions

    //constructor
    constructor() {
        supervisor = 0xFb8E7ef8453Ff07815f53D3697614bacf77dc76a;
        operator = 0x3deea4dc72f6735374C26AAE49939F375e790F07;

        state = WSNstate.dormant; //so when the contract is deployed the WSN is dormant and awaits deployment
    }

    function WSN_deployment() public OnlyOperator {
        require(state == WSNstate.dormant);
        state = WSNstate.deployed_in_plug_and_play; //operator deploys the WSN in plug and play orientation in routine monitoring
        emit WSN_deployed_in_plug_and_play(msg.sender);
    }

    function state_estimation() public OnlyOperator {
        if (state == WSNstate.deployed_in_plug_and_play)
            estimate = "calculating yet";
        else if (state == WSNstate.estimate_recorded) estimate = "recorded";
        else if (state == WSNstate.invalid_estimate) estimate = "invalid";
    }

    function record_state_estimate(int256 se) public OnlyOperator {
        require(state == WSNstate.deployed_in_plug_and_play);
        stateEstimate = se;
        state = WSNstate.estimate_recorded;
        emit estimate_recorded(msg.sender);
    }

    function check_for_anomalies() public OnlyOperator {
        if (stateEstimate >= 0 && stateEstimate <= 10) {
            state == WSNstate.invalid_estimate;
            emit invalid_estimate(msg.sender);
            revert invalid_Estimate(stateEstimate);
        } else if (stateEstimate >= 11 && stateEstimate <= 50) {
            emit no_anomaly_is_detected(msg.sender);
            anomaly_detected = false;
        } else if (stateEstimate >= 51 && stateEstimate <= 70) {
            emit anomaly_is_detected(msg.sender);
            anomaly_detected = true;
            anomaly_type = anomalyType.type1;
            emit type1anomaly_detected(msg.sender, stateEstimate);
        } else if (stateEstimate >= 71 && stateEstimate <= 80) {
            emit anomaly_is_detected(msg.sender);
            anomaly_detected = true;
            anomaly_type = anomalyType.type2;
            emit type2anomaly_detected(msg.sender, stateEstimate);
        } else if (stateEstimate >= 81 && stateEstimate <= 90) {
            emit anomaly_is_detected(msg.sender);
            anomaly_detected = true;
            anomaly_type = anomalyType.type3;
            emit type3anomaly_detected(msg.sender, stateEstimate);
        }
    }

    //what happens after an anomaly is detected is taken care of by the supervisor

    function deploy_WSN_fully() public OnlySupervisor {
        state = WSNstate.deployed_fully;
        emit WSN_deployed_fully(msg.sender);
    }

    function confirm_anomalies() public OnlySupervisor {
        if (stateEstimate >= 0 && stateEstimate <= 10) {
            state == WSNstate.invalid_estimate;
            emit invalid_estimate(msg.sender);
            revert invalid_Estimate(stateEstimate);
        } else if (stateEstimate >= 11 && stateEstimate <= 50) {
            emit no_anomaly_is_detected(msg.sender);
            anomaly_detected = false;
        } else if (stateEstimate >= 51 && stateEstimate <= 70) {
            emit anomaly_is_detected(msg.sender);
            anomaly_detected = true;
            anomaly_type = anomalyType.type1;
            emit type1anomaly_detected(msg.sender, stateEstimate);
        } else if (stateEstimate >= 71 && stateEstimate <= 80) {
            emit anomaly_is_detected(msg.sender);
            anomaly_detected = true;
            anomaly_type = anomalyType.type2;
            emit type2anomaly_detected(msg.sender, stateEstimate);
        } else if (stateEstimate >= 81 && stateEstimate <= 90) {
            emit anomaly_is_detected(msg.sender);
            anomaly_detected = true;
            anomaly_type = anomalyType.type3;
            emit type3anomaly_detected(msg.sender, stateEstimate);
        }
    }

    function raise_alarm() public OnlySupervisor {
        if (anomaly_detected == true) {
            emit anomaly_confirmed(msg.sender);
            emit alarm_raised(msg.sender);
        } else {
            emit no_anomaly_is_detected(msg.sender);
            state = WSNstate.deployed_in_plug_and_play;
        }
    }

    //getter functions are as follows:

    function view_estimate() public returns (int256) {
        times_visited[msg.sender] = times_visited[msg.sender] + 1;
        return stateEstimate;
    }

    function view_state_of_WSN() public view returns (WSNstate) {
        return state;
    }

    function view_state_of_estimate() public view returns (string memory) {
        return estimate;
    }

    function view_times_visited(address add) public returns (uint256) {
        times_visited_by = times_visited[add];
        return times_visited_by;
    }

    function view_anomaly_detected() public view returns (bool) {
        return anomaly_detected;
    }

    function view_anomaly_type() public view returns (anomalyType) {
        return anomaly_type;
    }
}
