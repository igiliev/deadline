import React from 'react'
import PropTypes from 'prop-types'
import {Tabs, Tab} from 'material-ui/Tabs'
import {getTopSolutions, getChallengeDetails, getAllUserSolutions} from './requests.js'
import ChallengeBoard from './ChallengeBoard.js'
import SubmissionsTable from './semantic_ui_components/SubmissionsTable.js'
import LeaderboardTable from './semantic_ui_components/LeaderboardTable.js'
import { Container } from 'semantic-ui-react'
import SwipeableViews from 'react-swipeable-views'

class ChallengeDetails extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      id: undefined,
      name: undefined,
      rating: undefined,
      score: undefined,
      description: {
        content: undefined,
        input_format: undefined,
        output_format: undefined,
        constraints: undefined,
        sample_input: undefined,
        sample_output: undefined,
        explanation: undefined
      },
      test_case_count: undefined,
      category: undefined,
      supported_languages: [],
      solutions: [],
      topSolutions: [],
      slideIndex: 0
    }

    this.loadChallengeDetails = this.loadChallengeDetails.bind(this)
    this.loadTopSubmissions = this.loadTopSubmissions.bind(this)
    this.handleTabChange = this.handleTabChange.bind(this)
    this.loadChallengeDetails()
  }

  loadChallengeDetails () {
    getChallengeDetails(this.props.match.params.challengeId).then(challenge => {
      this.setState(challenge)
      this.loadSubmissions(challenge.id)
      this.loadTopSubmissions(challenge.id)
    }).catch(err => {
      throw err  // TODO: handle
    })
  }

  loadSubmissions (challengeId) {
    getAllUserSolutions(challengeId).then(solutions => {
      this.setState({solutions})
    }).catch(err => {
      throw err
    })
  }

  loadTopSubmissions (challengeId) {
    getTopSolutions(challengeId).then(solutions => {
      this.setState({topSolutions: solutions})
    }).catch(err => {
      throw err
    })
  }

  handleTabChange (value, e) {
    this.setState({
      slideIndex: value
    })
  }

  render () {
    const styles = {
      headline: {
        fontSize: 24,
        paddingTop: 16,
        marginBottom: 12,
        fontWeight: 400
      },
      slide: {
        padding: 10
      }
    }
    return (
      <div>
        <Container>
          <Tabs
            onChange={this.handleTabChange}
            value={this.state.slideIndex}
            className='challenge-details-tab'
            tabItemContainerStyle={{background: '#303336'}}
            inkBarStyle={{color: '#f55333'}}
          >
            <Tab label='Challenge' value={0} onClick={() => { this.handleTabChange(0) }} buttonStyle={{fontWeight: 'bold'}} />
            <Tab label='Submissions' value={1} onClick={() => { this.handleTabChange(1) }} buttonStyle={{fontWeight: 'bold'}} />
            <Tab label='Leaderboard' value={2} onClick={() => { this.handleTabChange(2) }} buttonStyle={{fontWeight: 'bold'}} />
          </Tabs>
          <SwipeableViews
            index={this.state.slideIndex}
            onChangeIndex={this.handleTabChange}
          >
            <div>
              <ChallengeBoard {...this.state} />
            </div>
            <div style={styles.slide}>
              <SubmissionsTable maxScore={this.state.score} submissions={this.state.solutions} />
            </div>
            <div style={styles.slide}>
              <LeaderboardTable maxScore={this.state.score} submissions={this.state.topSolutions} />
            </div>
          </SwipeableViews>
        </Container>
      </div>
    )
  }
}

ChallengeDetails.propTypes = {
  match: PropTypes.shape({
    params: PropTypes.shape({
      challengeId: PropTypes.string.isRequired
    })
  })
}

export default ChallengeDetails