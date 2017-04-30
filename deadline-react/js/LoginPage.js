import React from 'react'
import LoginForm from './LoginForm'
import RegisterForm from './RegisterForm'
import Video from './Video'
import axios from 'axios'

class LoginPage extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      user: {
        username: '',
        email: '',
        password: '',
        repeatedPassword: ''
      }
    }

    this.processLoginForm = this.processLoginForm.bind(this)
    this.processRegisterForm = this.processRegisterForm.bind(this)
    this.handleLoginData = this.handleLoginData.bind(this)
    this.handleRegisterData = this.handleRegisterData.bind(this)
  }

  handleLoginData (e) {
    const field = e.target.name
    const user = this.state.user
    user[field] = e.target.value

    this.setState({
      user
    })
  }

  handleRegisterData (e) {
    const field = e.target.name
    const user = this.state.user
    user[field] = e.target.value
    // TODO compare passwords & validate data

    this.setState({
      user
    })
  }

  processLoginForm (e) {
    e.preventDefault()
    let user = this.state.user

    axios.post('http://localhost:8000/accounts/login/', {
      email: user.email,
      password: user.password
    })
    .then(resp => (
      console.log(resp)
    ))
  }

  processRegisterForm (e) {
    e.preventDefault()

    let user = this.state.user

    axios.post('http://localhost:8000/accounts/register/', {
      username: user.username,
      email: user.email,
      password: user.password
    })
    .then(resp => {
      console.log(resp)
    })
  }

  render () {
    return (
      <div>
        <div className='login-wrap'>
          <div className='login-html'>
            <input
              id='tab-1'
              type='radio'
              name='tab'
              className='sign-in'
              defaultChecked
            />
            <label htmlFor='tab-1' className='tab'>Sign In</label>
            <input
              id='tab-2'
              type='radio'
              name='tab'
              className='sign-up'
            />
            <label htmlFor='tab-2' className='tab'>Sign Up</label>
            <div className='form-container'>
              <LoginForm
                onSubmit={this.processLoginForm}
                onChange={this.handleLoginData}
                />
              <RegisterForm
                onSubmit={this.processRegisterForm}
                onChange={this.handleRegisterData}
              />
            </div>
          </div>
        </div>
        <Video />
      </div>
    )
  }
}

export default LoginPage
